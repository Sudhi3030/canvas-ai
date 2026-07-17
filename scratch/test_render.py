import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

SAMPLE_JSON = {
  "canvas": {
    "width": 800,
    "height": 800,
    "background_color": "#F3F4F6",
    "unit": "px"
  },
  "elements": [
    {
      "id": "bg_decoration",
      "name": "Background Shape",
      "type": "shape",
      "x": -50,
      "y": -50,
      "width": 300,
      "height": 300,
      "rotation": 45,
      "z_index": 1,
      "opacity": 0.5,
      "properties": {
        "fill_color": "#3B82F6",
        "border_radius": 20
      }
    },
    {
      "id": "hero_placeholder",
      "name": "Main Banner Image",
      "type": "image",
      "x": 100,
      "y": 150,
      "width": 600,
      "height": 350,
      "rotation": 0,
      "z_index": 2,
      "opacity": 1.0,
      "properties": {
        "url": "https://picsum.photos/600/350",
        "alt_text": "Placeholder banner"
      }
    },
    {
      "id": "title_text",
      "name": "Heading Text",
      "type": "text",
      "x": 100,
      "y": 550,
      "width": 600,
      "height": 80,
      "rotation": -2.0,
      "z_index": 3,
      "opacity": 1.0,
      "properties": {
        "content": "Supercharge Your Designs!",
        "font_family": "Arial",
        "font_size": 42,
        "font_weight": "bold",
        "color": "#111827"
      }
    },
    {
      "id": "cta_button",
      "name": "CTA Button",
      "type": "button",
      "x": 250,
      "y": 660,
      "width": 300,
      "height": 70,
      "rotation": 0,
      "z_index": 4,
      "opacity": 1.0,
      "properties": {
        "content": "Claim 50% Offer Now",
        "font_family": "Arial",
        "font_size": 20,
        "font_weight": "bold",
        "text_color": "#FFFFFF",
        "fill_color": "#EF4444",
        "border_radius": 12
      }
    }
  ],
  "metadata": {
    "created_by": "Architect Design Review",
    "template": "Promo Banner v1",
    "version": "1.0"
  }
}

def main():
    print("Parsing & Validating Sample Design JSON...")
    layout_obj = validate_layout(SAMPLE_JSON)
    print("Validation OK.")

    print("\nInitializing CanvasRenderer...")
    renderer = CanvasRenderer()
    
    print("\nRendering Layout...")
    output_img_path = renderer.render(layout_obj, filename="promo_banner.png")
    
    print(f"\n✓ Success! Image rendered and stored at: {output_img_path}")
    assert os.path.exists(output_img_path), "Error: Output PNG file was not written to outputs/images!"
    print("✓ Output verification complete.")

if __name__ == "__main__":
    main()
