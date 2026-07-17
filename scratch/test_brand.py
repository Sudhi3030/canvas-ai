import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateEngine
from design_engine.renderer.canvas_renderer import CanvasRenderer

def main():
    print("=== Testing Brand Kit & Template Engine ===")
    
    # 1. Instantiate Cafe Brand identity
    cafe_brand = BrandKit(
        name="Artisan Cafe",
        primary_color="#3E2723",     # Dark Brown
        secondary_color="#5D4037",   # Medium Brown
        accent_color="#FFD54F",      # Warm Amber/Gold
        font_heading="Arial",
        font_body="Arial",
        border_radius_default=32,
        logo_url="https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=100&q=80"  # Small coffee cup placeholder
    )
    
    print(f"Branded Identity: '{cafe_brand.name}' Initialized.")

    # 2. Build Instagram Layout
    print("\nGenerating branded Instagram layout...")
    ig_layout = TemplateEngine.create_branded_layout(
        template_name="Instagram",
        brand=cafe_brand,
        heading_text="MORNING BREW",
        body_text="Start your day with our freshly roasted espresso blends. Locally sourced, hand-crafted."
    )
    
    assert ig_layout.canvas.width == 1080
    assert ig_layout.canvas.height == 1080
    assert ig_layout.canvas.background_color == "#3E2723"
    print("✓ Square Instagram layout structure generated and validated.")

    # 3. Build Pinterest Layout
    print("Generating branded Pinterest layout...")
    pin_layout = TemplateEngine.create_branded_layout(
        template_name="Pinterest",
        brand=cafe_brand,
        heading_text="ARTISAN BAKERY",
        body_text="Sourdough loaves baked daily before sunrise. Warm, crusty, and perfect."
    )
    
    assert pin_layout.canvas.width == 1000
    assert pin_layout.canvas.height == 1500
    print("✓ Portrait Pinterest layout structure generated and validated.")

    # 4. Render Layouts
    print("\nRendering styled designs...")
    try:
        renderer = CanvasRenderer()
        ig_path = renderer.render(ig_layout, filename="test_brand_instagram.png")
        pin_path = renderer.render(pin_layout, filename="test_brand_pinterest.png")
        print(f"✓ Square Instagram banner written: {ig_path}")
        print(f"✓ Portrait Pinterest pin written: {pin_path}")
        
        # Verify card background inherits brand kit properties
        ig_card_bg = ig_layout.scene_tree[0].children[0]
        assert ig_card_bg.properties.fill_color == "#5D4037", "Card fill color does not match secondary brand color!"
        assert ig_card_bg.properties.border_radius == 32, "Card border radius does not match brand kit default!"
        print("✓ Rendering geometry inherits brand kit variables.")
        print("=== Brand Engine Test Passed ===")
    except Exception as e:
        print(f"✗ Rendering branded templates failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
