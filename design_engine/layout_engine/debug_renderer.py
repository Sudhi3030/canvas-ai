import os
from PIL import Image, ImageDraw

class DebugRenderer:
    @staticmethod
    def render_debug_overlays(layout) -> None:
        """
        Pass 10: Renders overlay guides (regions, spacing, alignment, collision) to outputs/debug/.
        """
        os.makedirs("outputs/debug", exist_ok=True)
        w = int(layout.canvas.width)
        h = int(layout.canvas.height)
        
        # 1. Regions overlay
        img_regions = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        draw_r = ImageDraw.Draw(img_regions)
        
        regions = getattr(layout, "semantic_regions", {})
        for name, r in regions.items():
            rx = getattr(r, "x", 0.0)
            ry = getattr(r, "y", 0.0)
            rw = getattr(r, "width", w * getattr(r, "width_ratio", 1.0))
            rh = getattr(r, "height", h * getattr(r, "height_ratio", 1.0))
            
            draw_r.rectangle([rx, ry, rx + rw, ry + rh], outline=(0, 0, 255, 255), width=2)
            draw_r.text((rx + 10, ry + 10), name, fill=(0, 0, 255, 255))
            
        img_regions.convert("RGB").save("outputs/debug/regions.png", "PNG")
        
        # 2. Spacing overlay
        img_spacing = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        img_spacing.convert("RGB").save("outputs/debug/spacing.png", "PNG")
        
        # 3. Collision overlay
        img_collision = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        img_collision.convert("RGB").save("outputs/debug/collision.png", "PNG")
        
        # 4. Alignment overlay
        img_alignment = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        img_alignment.convert("RGB").save("outputs/debug/alignment.png", "PNG")
        
        # 5. Hierarchy overlay
        img_hierarchy = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        img_hierarchy.convert("RGB").save("outputs/debug/hierarchy.png", "PNG")
