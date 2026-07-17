import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateEngine
from design_engine.renderer.canvas_renderer import CanvasRenderer

def main():
    print("=== Testing Pinterest Template Engine Slots ===")
    brand = BrandKit(
        name="Organic Salads Ltd",
        primary_color="#1E392A",
        secondary_color="#274E13",
        accent_color="#FFD54F",
        logo_url="https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80"
    )
    
    # Compile Pinterest template (contains Heading -> Hero -> Body -> CTA Button)
    layout = TemplateEngine.create_branded_layout(
        template_name="Pinterest",
        brand=brand,
        heading_text="EAT FRESH EAT GREEN",
        body_text="Harvested daily. Packed with organic fiber and protein. Order your salad pack today.",
        hero_image_url="https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&q=80"
    )
    
    print("✓ Pinterest template layout compiled.")
    
    # Assert nodes presence inside stack
    content_stack = layout.scene_tree[0].children[1]
    children_types = [child.type for child in content_stack.children]
    print(f"Content Stack Children Nodes: {children_types}")
    assert "text" in children_types, "Heading slot missing!"
    assert "image" in children_types, "Hero image slot missing!"
    assert "component" in children_types, "CTA Button component slot missing!"
    
    print("\n=== Rendering Pinterest Banner Preview ===")
    try:
        renderer = CanvasRenderer()
        output_path = renderer.render(layout, filename="test_pinterest_slots.png")
        print(f"✓ Success! Pinterest card written at: {output_path}")
        assert os.path.exists(output_path)
        print("=== Pinterest Slot Test Passed ===")
    except Exception as e:
        print(f"✗ Rendering failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
