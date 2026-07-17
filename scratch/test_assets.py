import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

# Assets showcase template using a public sample image
SAMPLE_IMAGE = "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=400&q=80"

TEST_ASSET_LAYOUT = {
  "canvas": {
    "width": 1000,
    "height": 1000,
    "background_color": "#1E293B",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "assets_grid",
      "name": "Assets Grid Container",
      "type": "group",
      "x": 50,
      "y": 50,
      "width": 900,
      "height": 900,
      "layout_mode": "absolute",
      "z_index": 1,
      "children": [
        {
          "id": "img_cover",
          "name": "Cover Image Node",
          "type": "image",
          "x": 0, "y": 0, "width": 400, "height": 400,
          "z_index": 2,
          "properties": {
            "url": SAMPLE_IMAGE,
            "fit_mode": "cover",
            "border_radius": 32
          }
        },
        {
          "id": "img_contain",
          "name": "Contain Image Node",
          "type": "image",
          "x": 450, "y": 0, "width": 450, "height": 400,
          "z_index": 3,
          "properties": {
            "url": SAMPLE_IMAGE,
            "fit_mode": "contain",
            "border_radius": 0
          }
        },
        {
          "id": "img_circular_filtered",
          "name": "Circular Filtered Image",
          "type": "image",
          "x": 0, "y": 450, "width": 400, "height": 400,
          "z_index": 4,
          "properties": {
            "url": SAMPLE_IMAGE,
            "fit_mode": "cover",
            "clip_circle": True,
            "brightness": 1.2,
            "contrast": 1.5,
            "saturation": 2.0,
            "blur": 3.0
          }
        },
        {
          "id": "img_description",
          "name": "Label Text",
          "type": "text",
          "x": 450, "y": 450, "width": 450, "height": 400,
          "z_index": 5,
          "properties": {
            "content": "Image Engine: Cover with 32px rounded corners (Top-Left)\n\nContain fit maintaining ratio (Top-Right)\n\nCircular mask + saturation + blur filters (Bottom-Left)",
            "font_family": "Arial",
            "font_size": 24.0,
            "color": "#F8FAFC",
            "align": "left",
            "line_height": 1.6
          }
        }
      ]
    }
  ],
  "metadata": {
    "created_by": "Design Assets Engine Phase 4",
    "template": "Assets Filters Showcase",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Assets Engine Parser & Validator ===")
    try:
        layout = validate_layout(TEST_ASSET_LAYOUT)
        print("✓ Pydantic verified Image and asset properties.")
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
        sys.exit(1)

    print("\n=== Rendering Assets & Filters Showcase ===")
    try:
        renderer = CanvasRenderer()
        output_path = renderer.render(layout, filename="test_assets_filters.png")
        print(f"✓ Success! Assets layout rendered preview: {output_path}")
        assert os.path.exists(output_path), "Error: Preview image not found!"
        print("=== Assets Engine Test Passed ===")
    except Exception as e:
        print(f"✗ Assets renderer failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
