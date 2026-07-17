import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

TEST_VISUALS_LAYOUT = {
  "canvas": {
    "width": 800,
    "height": 800,
    "background_color": "#0F172A",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "gradient_card",
      "name": "Linear Gradient Card with Inner Shadow",
      "type": "shape",
      "x": 200, "y": 200, "width": 400, "height": 400,
      "z_index": 1,
      "effects": [
        {
          "type": "drop_shadow",
          "color": "#000000",
          "offset_x": 0.0,
          "offset_y": 16.0,
          "blur": 32.0
        },
        {
          "type": "inner_shadow",
          "color": "#000000",
          "offset_x": 4.0,
          "offset_y": 4.0,
          "blur": 12.0
        }
      ],
      "properties": {
        "fill_color": "#CCCCCC", # Fallback
        "border_radius": 32,
        "fill_gradient": {
          "colors": ["#F59E0B", "#EF4444"], # Amber to Red
          "angle": 90.0
        }
      }
    }
  ],
  "metadata": {
    "created_by": "Visual Effects Phase 5",
    "template": "Visual Test",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Visual Effects Validator ===")
    try:
        layout = validate_layout(TEST_VISUALS_LAYOUT)
        print("✓ Visual effects layout validation succeeded.")
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        sys.exit(1)

    print("\n=== Rendering Visual Effects Preview ===")
    try:
        renderer = CanvasRenderer()
        output_path = renderer.render(layout, filename="test_visual_effects.png")
        print(f"✓ Success! Visual effects card rendered at: {output_path}")
        assert os.path.exists(output_path)
        print("=== Visual Effects Test Passed ===")
    except Exception as e:
        print(f"✗ Rendering failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
