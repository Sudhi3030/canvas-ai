import logging
from typing import List, Tuple
from PIL import ImageDraw
from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, TextNode, GroupNode, ShapeNode
from design_engine.layout_engine.layout import wrap_text

logger = logging.getLogger("DesignRulesEngine")

def relative_luminance(color_hex: str) -> float:
    # Convert hex color string to relative luminance value
    from design_engine.renderer.canvas_renderer import hex_to_rgba
    rgba = hex_to_rgba(color_hex)
    rgb = [c / 255.0 for c in rgba[:3]]
    # Adjust for sRGB gamma curve
    adjusted = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * adjusted[0] + 0.7152 * adjusted[1] + 0.0722 * adjusted[2]

def contrast_ratio(hex1: str, hex2: str) -> float:
    y1 = relative_luminance(hex1)
    y2 = relative_luminance(hex2)
    bright = max(y1, y2)
    dark = min(y1, y2)
    return (bright + 0.05) / (dark + 0.05)

class DesignRulesEngine:
    def __init__(self):
        from PIL import Image
        self.dummy_img = Image.new("RGBA", (1, 1))
        self.dummy_draw = ImageDraw.Draw(self.dummy_img)

    def analyze_and_fix(self, layout: Layout) -> List[str]:
        """
        Runs validations and applies automatic layout repairs.
        Returns a list of warnings resolved.
        """
        resolved_warnings = []
        canvas_w = float(layout.canvas.width)
        canvas_h = float(layout.canvas.height)
        canvas_bg = layout.canvas.background_color

        # Traverse and fix nodes
        for node in layout.scene_tree:
            self._fix_node_recursive(node, 0.0, 0.0, canvas_w, canvas_h, canvas_bg, resolved_warnings)
        
        # Typographic hierarchy check (Heading size must exceed Body size by at least 1.5x)
        headings = []
        bodies = []
        
        def find_text_nodes(n: Node):
            if isinstance(n, TextNode):
                nid = n.id.lower()
                nname = n.name.lower()
                if "heading" in nid or "header" in nid or "title" in nid or "heading" in nname or "title" in nname:
                    headings.append(n)
                elif "body" in nid or "desc" in nid or "copy" in nid or "body" in nname or "desc" in nname:
                    bodies.append(n)
            elif isinstance(n, GroupNode):
                for child in n.children:
                    find_text_nodes(child)
                    
        for root in layout.scene_tree:
            find_text_nodes(root)
            
        for h in headings:
            for b in bodies:
                if h.properties.font_size < b.properties.font_size * 1.5:
                    old_h_size = h.properties.font_size
                    new_h_size = b.properties.font_size * 1.5
                    h.properties.font_size = new_h_size
                    resolved_warnings.append(
                        f"Corrected broken typographic hierarchy: Boosted heading '{h.name}' font size "
                        f"from {old_h_size:.1f}pt to {new_h_size:.1f}pt (must exceed body '{b.name}' by 1.5x)."
                    )
                    
        return resolved_warnings

    def _fix_node_recursive(self, node: Node, parent_x: float, parent_y: float, canvas_w: float, canvas_h: float, parent_bg: str, warnings: List[str]) -> None:
        # Hidden CTA button fixer
        if "cta" in node.id.lower() or "button" in node.id.lower():
            if not node.visible or node.opacity < 0.2:
                node.visible = True
                node.opacity = 1.0
                warnings.append(f"Auto-restored hidden CTA button '{node.name}' to fully visible and opaque.")

        if not node.visible:
            return

        world_x = parent_x + node.x
        world_y = parent_y + node.y

        # 1. Canvas Boundary Clamp
        if world_x < 0:
            shift = -world_x
            node.x += shift
            world_x = 0.0
            warnings.append(f"Clamped '{node.name}' inside left canvas margin (shifted by {shift:.1f}px).")
        elif world_x + node.width > canvas_w:
            shift = (world_x + node.width) - canvas_w
            node.x -= shift
            world_x -= shift
            warnings.append(f"Clamped '{node.name}' inside right canvas margin (shifted by {shift:.1f}px).")

        if world_y < 0:
            shift = -world_y
            node.y += shift
            world_y = 0.0
            warnings.append(f"Clamped '{node.name}' inside top canvas margin (shifted by {shift:.1f}px).")
        elif world_y + node.height > canvas_h:
            shift = (world_y + node.height) - canvas_h
            node.y -= shift
            world_y -= shift
            warnings.append(f"Clamped '{node.name}' inside bottom canvas margin (shifted by {shift:.1f}px).")

        # Resolve local backgrounds
        current_bg = parent_bg
        if isinstance(node, ShapeNode) and node.properties.fill_color:
            current_bg = node.properties.fill_color

        # 2. Text Specific Rules (Contrast, Auto-Shrink, Legibility)
        if isinstance(node, TextNode):
            # Legibility: Bump up tiny font sizes (< 10pt) to 12pt
            if node.properties.font_size < 10.0:
                old_sz = node.properties.font_size
                node.properties.font_size = 12.0
                warnings.append(f"Auto-fixed tiny font size for '{node.name}' from {old_sz:.1f}pt to 12.0pt to ensure legibility.")

            # A. Contrast Check (WCAG thresholds: 3.0:1 for size >= 18pt, 4.5:1 otherwise)
            text_color = node.properties.color
            ratio = contrast_ratio(text_color, current_bg)
            required_ratio = 3.0 if node.properties.font_size >= 18.0 else 4.5
            
            if ratio < required_ratio:
                # Contrast violation: Auto-fix by forcing color shift
                bg_luminance = relative_luminance(current_bg)
                new_color = "#FFFFFF" if bg_luminance < 0.5 else "#0F172A"
                node.properties.color = new_color
                warnings.append(
                    f"Contrast ratio ({ratio:.1f}:1) for '{node.name}' on background '{current_bg}' was below WCAG threshold ({required_ratio:.1f}:1). "
                    f"Auto-fixed text color to '{new_color}'."
                )

            # B. Text Box Height Overflow Auto-Shrink
            if node.height_policy == "fixed":
                from design_engine.renderer.canvas_renderer import load_font
                font = load_font(node.properties.font_family, node.properties.font_size)
                lines = wrap_text(node.properties.content, font, node.width, node.properties.letter_spacing)
                bbox = self.dummy_draw.textbbox((0, 0), "Ap", font=font)
                line_h = bbox[3] - bbox[1]
                required_h = len(lines) * line_h * node.properties.line_height

                # Loop to shrink font size if text overflows height limits
                original_size = node.properties.font_size
                min_font_size = 12.0
                while required_h > node.height and node.properties.font_size > min_font_size:
                    node.properties.font_size -= 2.0
                    font = load_font(node.properties.font_family, node.properties.font_size)
                    lines = wrap_text(node.properties.content, font, node.width, node.properties.letter_spacing)
                    bbox = self.dummy_draw.textbbox((0, 0), "Ap", font=font)
                    line_h = bbox[3] - bbox[1]
                    required_h = len(lines) * line_h * node.properties.line_height

                if node.properties.font_size < original_size:
                    warnings.append(
                        f"Auto-shrunk font size for '{node.name}' from {original_size:.1f}pt to {node.properties.font_size:.1f}pt "
                        f"to prevent boundary height overflow."
                    )

        # 3. Recurse children
        if isinstance(node, GroupNode):
            # Safe vertical overlap fix (push apart elements that crash vertically in absolute groups)
            if node.layout_mode == "absolute" and len(node.children) > 1:
                # Simple absolute overlap corrector
                sorted_by_y = sorted(node.children, key=lambda n: n.y)
                for i in range(len(sorted_by_y) - 1):
                    curr = sorted_by_y[i]
                    nxt = sorted_by_y[i+1]
                    # Check overlap boundaries (skip if either is a background card shape)
                    if curr.z_index == 0 or nxt.z_index == 0 or "bg" in curr.id or "bg" in nxt.id:
                        continue
                    if curr.y + curr.height > nxt.y:
                        clash_y = (curr.y + curr.height) - nxt.y
                        nxt.y += clash_y
                        warnings.append(f"Auto-shifted overlap clash: Pushed '{nxt.name}' down by {clash_y:.1f}px.")

            for child in node.children:
                self._fix_node_recursive(child, world_x, world_y, canvas_w, canvas_h, current_bg, warnings)
