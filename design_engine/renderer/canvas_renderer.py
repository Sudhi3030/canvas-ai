import os
import httpx
from io import BytesIO
from typing import Tuple, List, Union, Any
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from design_engine.config import CONFIG
from design_engine.scene_graph.document import Layout, Canvas
from design_engine.scene_graph.node import Node, TextNode, ImageNode, ShapeNode, GroupNode
from design_engine.layout_engine.layout import LayoutSolver

# Caching registries to prevent disk/network bottlenecks
_IMAGE_CACHE = {}
_GRADIENT_CACHE = {}

BASE_DIR = CONFIG.BASE_DIR
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

def hex_to_rgba(hex_str: str, opacity: float = 1.0) -> Tuple[int, int, int, int]:
    """
    Utility to convert hex code strings to (R, G, B, A) channels.
    """
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = "".join(c*2 for c in hex_str)
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    a = int(opacity * 255)
    return (r, g, b, a)

@lru_cache(maxsize=256)
def load_font(font_family: str, size: float) -> ImageFont.ImageFont:
    """
    Loads font faces from local directory assets or falls back to system matches/defaults.
    """
    font_filename = f"{font_family}.ttf"
    local_font_path = os.path.join(FONTS_DIR, font_filename)
    
    # Try local asset fonts first
    if os.path.exists(local_font_path):
        try:
            return ImageFont.truetype(local_font_path, int(size))
        except Exception:
            pass

    # Try common system paths for macOS/Linux/Windows fallbacks
    system_font_paths = [
        f"/Library/Fonts/{font_family}.ttf",
        f"/System/Library/Fonts/Supplemental/{font_family}.ttf",
        f"/System/Library/Fonts/{font_family}.ttf",
        f"/usr/share/fonts/truetype/dejavu/{font_family}.ttf",
        f"/usr/share/fonts/TTF/{font_family}.ttf",
        f"C:\\Windows\\Fonts\\{font_family}.ttf"
    ]
    
    for path in system_font_paths:
        try:
            return ImageFont.truetype(path, int(size))
        except Exception:
            continue
    return ImageFont.load_default()

class CanvasRenderer:
    def __init__(self, output_dir: str = "outputs/images"):
        self.output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def create_canvas(self, canvas_settings: Canvas) -> Image.Image:
        bg_rgba = hex_to_rgba(canvas_settings.background_color, 1.0)
        return Image.new("RGBA", (canvas_settings.width, canvas_settings.height), bg_rgba)

    def render_to_image(self, layout: Layout) -> Image.Image:
        """
        Renders the design document scene graph onto a Pillow Image.
        """
        # Solve auto layout coordinates and sizes
        solver = LayoutSolver()
        solver.solve(layout)

        # Apply Design Rules & Auto-Correct constraints
        from design_engine.design_rules.accessibility import DesignRulesEngine
        rules = DesignRulesEngine()
        fixes = rules.analyze_and_fix(layout)
        for fix in fixes:
            print(f"[DesignRules Auto-Fix] {fix}")

        # Create base empty canvas image
        canvas_img = self.create_canvas(layout.canvas)
        
        # Sort root nodes by z-index
        sorted_roots = sorted(layout.scene_tree, key=lambda n: n.z_index)

        # Recursively render nodes starting with parent offset (0, 0)
        for node in sorted_roots:
            self._render_node_recursive(canvas_img, node, parent_x=0.0, parent_y=0.0, parent_opacity=1.0, parent_rotation=0.0)

        # Convert to RGB standard
        final_rgb = Image.new("RGB", canvas_img.size, (255, 255, 255))
        final_rgb.paste(canvas_img, mask=canvas_img.split()[3])
        return final_rgb

    def render(self, layout: Layout, filename: str = "design_output.png") -> str:
        """
        Generates design canvas and saves it to output directories.
        """
        img = self.render_to_image(layout)
        save_path = os.path.join(self.output_dir, filename)
        img.save(save_path, "PNG")
        return save_path

    def _render_node_recursive(
        self,
        canvas_img: Image.Image,
        node: Node,
        parent_x: float,
        parent_y: float,
        parent_opacity: float,
        parent_rotation: float
    ) -> None:
        if not node.visible:
            return

        # Solve cumulative absolute transformations
        world_x = parent_x + node.x
        world_y = parent_y + node.y
        world_opacity = parent_opacity * node.opacity
        world_rotation = parent_rotation + node.rotation

        # Create a layer image representing this single element
        w, h = int(node.width), int(node.height)
        layer = None

        if isinstance(node, GroupNode):
            # Recurse children inside parent container relative offset context
            # Group nodes don't draw pixel masks directly but act as layout envelopes
            sorted_children = sorted(node.children, key=lambda n: n.z_index)
            for child in sorted_children:
                self._render_node_recursive(
                    canvas_img, child, 
                    parent_x=world_x, parent_y=world_y, 
                    parent_opacity=world_opacity, parent_rotation=world_rotation
                )
        else:
            # Draw leaf nodes
            layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            
            if isinstance(node, TextNode):
                draw = ImageDraw.Draw(layer)
                font = load_font(node.properties.font_family, node.properties.font_size)
                
                text_color = hex_to_rgba(node.properties.color, world_opacity)
                stroke_rgba = hex_to_rgba(node.properties.stroke_color, world_opacity) if node.properties.stroke_color else None
                # Disable legacy text character-level shadow drawing in favor of unified effects
                shadow_rgba = None

                # Segment paragraph content based on wrap boundaries
                from design_engine.layout_engine.layout import wrap_text
                lines = wrap_text(node.properties.content, font, node.width, node.properties.letter_spacing)
                
                # Retrieve bounding height of test metrics
                bbox = draw.textbbox((0, 0), "Ap", font=font)
                line_height_px = (bbox[3] - bbox[1]) * node.properties.line_height

                # Compute baseline vertical alignment
                total_text_h = len(lines) * line_height_px
                start_y = 0.0
                if node.properties.vertical_align == "middle":
                    start_y = (node.height - total_text_h) / 2
                elif node.properties.vertical_align == "bottom":
                    start_y = node.height - total_text_h

                for i, line in enumerate(lines):
                    line_y = start_y + (i * line_height_px)
                    
                    # Compute horizontal alignment
                    line_w = sum(font.getlength(c) for c in line) + node.properties.letter_spacing * (len(line) - 1)
                    line_x = 0.0
                    if node.properties.align == "center":
                        line_x = (node.width - line_w) / 2
                    elif node.properties.align == "right":
                        line_x = node.width - line_w

                    # Draw character by character if letter_spacing is applied
                    if node.properties.letter_spacing > 0:
                        char_x = line_x
                        for char in line:
                            char_w = font.getlength(char)
                            
                            # Draw Drop Shadow
                            if shadow_rgba:
                                draw.text(
                                    (char_x + node.properties.shadow_offset_x, line_y + node.properties.shadow_offset_y),
                                    char, font=font, fill=shadow_rgba
                                )
                            # Draw Character + Outline stroke
                            draw.text(
                                    (char_x, line_y), char, font=font, fill=text_color,
                                    stroke_width=node.properties.stroke_width, stroke_fill=stroke_rgba
                            )
                            char_x += char_w + node.properties.letter_spacing
                    else:
                        # Draw solid line
                        if shadow_rgba:
                            draw.text(
                                (line_x + node.properties.shadow_offset_x, line_y + node.properties.shadow_offset_y),
                                line, font=font, fill=shadow_rgba
                            )
                        draw.text(
                            (line_x, line_y), line, font=font, fill=text_color,
                            stroke_width=node.properties.stroke_width, stroke_fill=stroke_rgba
                        )
                
            elif isinstance(node, ImageNode):
                layer = self._draw_image_leaf(node)
                
            elif isinstance(node, ShapeNode):
                radius = node.properties.border_radius
                draw = ImageDraw.Draw(layer)
                
                fill_grad = node.properties.fill_gradient
                stroke = hex_to_rgba(node.properties.stroke_color, world_opacity) if node.properties.stroke_color else None
                stroke_w = node.properties.stroke_width
                
                if fill_grad:
                    shape_mask = Image.new("L", (w, h), 0)
                    mask_draw = ImageDraw.Draw(shape_mask)
                    if radius > 0:
                        mask_draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
                    else:
                        mask_draw.rectangle([0, 0, w, h], fill=255)
                    
                    gradient_img = self._create_linear_gradient(w, h, fill_grad.colors, fill_grad.angle, world_opacity)
                    layer.paste(gradient_img, (0, 0), mask=shape_mask)
                    
                    if stroke and stroke_w > 0:
                        if radius > 0:
                            draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=None, outline=stroke, width=stroke_w)
                        else:
                            draw.rectangle([0, 0, w, h], fill=None, outline=stroke, width=stroke_w)
                else:
                    fill = hex_to_rgba(node.properties.fill_color, world_opacity)
                    if radius > 0:
                        draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=fill, outline=stroke, width=stroke_w)
                    else:
                        draw.rectangle([0, 0, w, h], fill=fill, outline=stroke, width=stroke_w)

            # Apply unified effects (drop shadow, glow, blur)
            effects_to_run = list(getattr(node, "effects", []))
            
            # Fallback legacy parsing for backward compatibility
            if not effects_to_run:
                # Shape legacy shadow
                if isinstance(node, ShapeNode) and node.properties.shadow_color and node.properties.shadow_blur > 0:
                    from design_engine.scene_graph.node import ShadowEffect
                    effects_to_run.append(ShadowEffect(
                        type="drop_shadow",
                        color=node.properties.shadow_color,
                        offset_x=node.properties.shadow_offset_x,
                        offset_y=node.properties.shadow_offset_y,
                        blur=node.properties.shadow_blur
                    ))
                # Text legacy shadow
                elif isinstance(node, TextNode) and node.properties.shadow_color:
                    from design_engine.scene_graph.node import ShadowEffect
                    effects_to_run.append(ShadowEffect(
                        type="drop_shadow",
                        color=node.properties.shadow_color,
                        offset_x=node.properties.shadow_offset_x,
                        offset_y=node.properties.shadow_offset_y,
                        blur=4.0
                    ))

            # Apply the effects to the layer
            if effects_to_run and layer:
                layer = self._apply_node_effects(canvas_img, node, layer, world_x, world_y, world_opacity, effects_to_run)

            # Apply overall opacity multiplier if layer is active
            if world_opacity < 1.0 and layer:
                alpha = layer.split()[3]
                alpha = alpha.point(lambda p: int(p * world_opacity))
                layer.putalpha(alpha)

            # Apply cumulative rotation angle
            if world_rotation != 0.0 and layer:
                layer = layer.rotate(world_rotation, expand=True, resample=Image.Resampling.BICUBIC)
                
                # Retrieve offsets shift caused by rotation bounds expansion
                new_w, new_h = layer.size
                world_x -= (new_w - w) / 2
                world_y -= (new_h - h) / 2

            # Composite single visual element onto canvas image
            if layer:
                canvas_img.paste(layer, (int(world_x), int(world_y)), mask=layer)

    def _draw_image_leaf(self, node: ImageNode) -> Image.Image:
        from PIL import ImageEnhance, ImageFilter
        img_url = node.properties.url
        w, h = int(node.width), int(node.height)
        loaded_img = None
        
        if img_url:
            if img_url in _IMAGE_CACHE:
                loaded_img = _IMAGE_CACHE[img_url].copy()
            elif img_url.startswith("http://") or img_url.startswith("https://"):
                try:
                    response = httpx.get(img_url, timeout=5.0)
                    loaded_img = Image.open(BytesIO(response.content))
                    _IMAGE_CACHE[img_url] = loaded_img.copy()
                except Exception:
                    pass
            elif os.path.exists(img_url):
                try:
                    loaded_img = Image.open(img_url)
                    _IMAGE_CACHE[img_url] = loaded_img.copy()
                except Exception:
                    pass

        if not loaded_img:
            # Fallback placeholder cross card
            loaded_img = Image.new("RGBA", (w, h), (200, 200, 200, 255))
            draw = ImageDraw.Draw(loaded_img)
            draw.line([0, 0, w, h], fill=(120, 120, 120, 255), width=2)
            draw.line([0, h, w, 0], fill=(120, 120, 120, 255), width=2)
            draw.rectangle([0, 0, w-1, h-1], outline=(100, 100, 100, 255), width=1)
        
        loaded_img = loaded_img.convert("RGBA")
        sw, sh = loaded_img.size
        
        # 1. Apply Sizing Fit Modes (Cover, Contain, Fill)
        fit_mode = node.properties.fit_mode
        
        if fit_mode == "cover":
            rs = sw / sh
            rt = w / h
            if rs > rt:
                # Scale height to match, crop width
                scale_h = h
                scale_w = int(h * rs)
                scaled_img = loaded_img.resize((scale_w, scale_h), Image.Resampling.LANCZOS)
                crop_x = (scale_w - w) // 2
                processed_img = scaled_img.crop((crop_x, 0, crop_x + w, h))
            else:
                # Scale width to match, crop height
                scale_w = w
                scale_h = int(w / rs)
                scaled_img = loaded_img.resize((scale_w, scale_h), Image.Resampling.LANCZOS)
                crop_y = (scale_h - h) // 2
                processed_img = scaled_img.crop((0, crop_y, w, crop_y + h))
        elif fit_mode == "contain":
            rs = sw / sh
            rt = w / h
            processed_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            if rs > rt:
                # Fit width, letterbox height
                scale_w = w
                scale_h = int(w / rs)
                scaled_img = loaded_img.resize((scale_w, scale_h), Image.Resampling.LANCZOS)
                paste_y = (h - scale_h) // 2
                processed_img.paste(scaled_img, (0, paste_y))
            else:
                # Fit height, pillarbox width
                scale_h = h
                scale_w = int(h * rs)
                scaled_img = loaded_img.resize((scale_w, scale_h), Image.Resampling.LANCZOS)
                paste_x = (w - scale_w) // 2
                processed_img.paste(scaled_img, (paste_x, 0))
        else:  # "fill"
            processed_img = loaded_img.resize((w, h), Image.Resampling.LANCZOS)

        # 2. Apply Filters (Brightness, Contrast, Saturation, Blur)
        if node.properties.brightness != 1.0:
            processed_img = ImageEnhance.Brightness(processed_img).enhance(node.properties.brightness)
        if node.properties.contrast != 1.0:
            processed_img = ImageEnhance.Contrast(processed_img).enhance(node.properties.contrast)
        if node.properties.saturation != 1.0:
            processed_img = ImageEnhance.Color(processed_img).enhance(node.properties.saturation)
        if node.properties.blur > 0.0:
            processed_img = processed_img.filter(ImageFilter.GaussianBlur(node.properties.blur))

        # 3. Apply Clipping Masks (Circular Clip or Rounded Corners)
        mask = Image.new("L", (w, h), 0)
        mask_draw = ImageDraw.Draw(mask)
        has_mask = False

        if node.properties.clip_circle:
            mask_draw.ellipse((0, 0, w, h), fill=255)
            has_mask = True
        elif node.properties.border_radius > 0:
            mask_draw.rounded_rectangle((0, 0, w, h), radius=node.properties.border_radius, fill=255)
            has_mask = True

        if has_mask:
            final_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            final_img.paste(processed_img, (0, 0), mask=mask)
            return final_img

        return processed_img

    def _apply_node_effects(
        self,
        canvas_img: Image.Image,
        node: Node,
        layer: Image.Image,
        world_x: float,
        world_y: float,
        world_opacity: float,
        effects: List[Any]
    ) -> Image.Image:
        from PIL import ImageFilter
        
        for effect in effects:
            if effect.type == "drop_shadow":
                blur_radius = effect.blur
                margin = int(blur_radius * 2.5) if blur_radius > 0 else 0
                
                alpha = layer.split()[3]
                
                shadow_w = layer.width + margin * 2
                shadow_h = layer.height + margin * 2
                shadow_canvas = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
                
                shadow_rgba = hex_to_rgba(effect.color, world_opacity)
                shadow_canvas.paste(shadow_rgba, (margin, margin), mask=alpha)
                
                if blur_radius > 0:
                    shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(blur_radius))
                    
                sx = int(world_x + effect.offset_x - margin)
                sy = int(world_y + effect.offset_y - margin)
                canvas_img.paste(shadow_canvas, (sx, sy), mask=shadow_canvas)
                
            elif effect.type == "glow":
                blur_radius = effect.blur
                margin = int(blur_radius * 2.5) if blur_radius > 0 else 0
                
                alpha = layer.split()[3]
                glow_w = layer.width + margin * 2
                glow_h = layer.height + margin * 2
                glow_canvas = Image.new("RGBA", (glow_w, glow_h), (0, 0, 0, 0))
                
                glow_rgba = hex_to_rgba(effect.color, world_opacity)
                glow_canvas.paste(glow_rgba, (margin, margin), mask=alpha)
                
                if blur_radius > 0:
                    glow_canvas = glow_canvas.filter(ImageFilter.GaussianBlur(blur_radius))
                    
                gx = int(world_x - margin)
                gy = int(world_y - margin)
                canvas_img.paste(glow_canvas, (gx, gy), mask=glow_canvas)
                
            elif effect.type == "inner_shadow":
                from PIL import ImageChops
                blur_radius = effect.blur
                
                alpha = layer.split()[3]
                
                ox = int(effect.offset_x)
                oy = int(effect.offset_y)
                offset_mask = Image.new("L", layer.size, 0)
                offset_mask.paste(alpha, (ox, oy))
                
                inner_boundary = ImageChops.subtract(alpha, offset_mask)
                
                if blur_radius > 0:
                    margin = int(blur_radius * 2.5)
                    large_w = layer.width + margin * 2
                    large_h = layer.height + margin * 2
                    large_img = Image.new("L", (large_w, large_h), 0)
                    large_img.paste(inner_boundary, (margin, margin))
                    large_img = large_img.filter(ImageFilter.GaussianBlur(blur_radius))
                    inner_boundary = large_img.crop((margin, margin, margin + layer.width, margin + layer.height))
                
                shadow_rgba = hex_to_rgba(effect.color, world_opacity)
                shadow_tint = Image.new("RGBA", layer.size, shadow_rgba)
                
                layer.paste(shadow_tint, (0, 0), mask=inner_boundary)
                
            elif effect.type == "blur":
                if effect.radius > 0:
                    layer = layer.filter(ImageFilter.GaussianBlur(effect.radius))
                    
        return layer

    def _create_linear_gradient(self, w: int, h: int, colors: List[str], angle: float, opacity: float) -> Image.Image:
        cache_key = (w, h, tuple(colors), angle, opacity)
        if cache_key in _GRADIENT_CACHE:
            return _GRADIENT_CACHE[cache_key].copy()

        c1 = hex_to_rgba(colors[0], opacity)
        c2 = hex_to_rgba(colors[1], opacity)
        
        grad = Image.new("RGBA", (w, h))
        draw = ImageDraw.Draw(grad)
        
        # Simple vertical vs horizontal interpolation
        is_horizontal = abs(angle) < 45.0 or abs(angle) > 135.0
        
        if is_horizontal:
            for x in range(w):
                t = x / max(1, w - 1)
                r = int(c1[0] * (1 - t) + c2[0] * t)
                g = int(c1[1] * (1 - t) + c2[1] * t)
                b = int(c1[2] * (1 - t) + c2[2] * t)
                a = int(c1[3] * (1 - t) + c2[3] * t)
                draw.line([(x, 0), (x, h)], fill=(r, g, b, a))
        else:
            for y in range(h):
                t = y / max(1, h - 1)
                r = int(c1[0] * (1 - t) + c2[0] * t)
                g = int(c1[1] * (1 - t) + c2[1] * t)
                b = int(c1[2] * (1 - t) + c2[2] * t)
                a = int(c1[3] * (1 - t) + c2[3] * t)
                draw.line([(0, y), (w, y)], fill=(r, g, b, a))
                
        _GRADIENT_CACHE[cache_key] = grad.copy()
        return grad
