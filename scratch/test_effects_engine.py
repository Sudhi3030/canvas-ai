import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

TEST_EFFECTS_LAYOUT = {
  "canvas": {
    "width": 800,
    "height": 800,
    "background_color": "#0F172A",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "shadow_card",
      "name": "Card with Multiple Effects",
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
          "type": "glow",
          "color": "#38BDF8",
          "blur": 16.0
        }
      ],
      "properties": {
        "fill_color": "#1E293B",
        "border_radius": 24
      }
    },
    {
      "id": "glowing_text",
      "name": "Glowing Headline Text",
      "type": "text",
      "x": 250, "y": 380, "width": 300, "height": 60,
      "z_index": 2,
      "effects": [
        {
          "type": "glow",
          "color": "#FFD54F",
          "blur": 8.0
        }
      ],
      "properties": {
        "content": "GLOW EFFECT",
        "font_family": "Arial",
        "font_size": 36.0,
        "color": "#FFFFFF",
        "align": "center"
      }
    }
  ],
  "metadata": {
    "created_by": "Effects Engine Phase 1",
    "template": "Effects Test",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Effects Engine Validator ===")
    try:
        layout = validate_layout(TEST_EFFECTS_LAYOUT)
        print("✓ Pydantic verified multiple complex effects configurations.")
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        sys.exit(1)

    print("\n=== Rendering Visual Effects Preview ===")
    try:
        renderer = CanvasRenderer()
        output_path = renderer.render(layout, filename="test_effects_engine.png")
        print(f"✓ Success! Effects banner rendered at: {output_path}")
        assert os.path.exists(output_path)
        print("=== Effects Engine Test Passed ===")
    except Exception as e:
        print(f"✗ Rendering failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
