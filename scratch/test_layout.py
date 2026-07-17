import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

# Nested absolute container enclosing background + vertical stack flow
TEST_FLOW_LAYOUT = {
  "canvas": {
    "width": 800,
    "height": 800,
    "background_color": "#111827",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "main_card",
      "name": "Card Container",
      "type": "group",
      "x": 150,
      "y": 150,
      "width": 500,
      "height": 500,
      "layout_mode": "absolute",
      "z_index": 1,
      "children": [
        {
          "id": "card_bg",
          "name": "Card Background",
          "type": "shape",
          "x": 0,
          "y": 0,
          "width_policy": "fill",
          "height_policy": "fill",
          "z_index": 1,
          "properties": {
            "fill_color": "#1F2937",
            "border_radius": 24,
            "stroke_color": "#374151",
            "stroke_width": 2
          }
        },
        {
          "id": "content_stack",
          "name": "Content Stack",
          "type": "group",
          "x": 0,
          "y": 0,
          "width_policy": "fill",
          "height_policy": "fill",
          "layout_mode": "vertical",
          "spacing": 24.0,
          "padding_left": 40.0,
          "padding_right": 40.0,
          "padding_top": 40.0,
          "padding_bottom": 40.0,
          "cross_align": "center",
          "main_align": "center",
          "z_index": 2,
          "children": [
            {
              "id": "card_title",
              "name": "Header Text",
              "type": "text",
              "width_policy": "fit",
              "height_policy": "fit",
              "z_index": 2,
              "properties": {
                "content": "Flow Stack Card",
                "font_family": "Arial",
                "font_size": 32.0,
                "color": "#FFFFFF"
              }
            },
            {
              "id": "card_divider",
              "name": "Divider Line",
              "type": "shape",
              "width_policy": "fill",
              "height": 4.0,
              "z_index": 3,
              "properties": {
                "fill_color": "#EF4444",
                "border_radius": 2
              }
            },
            {
              "id": "card_description",
              "name": "Body Text",
              "type": "text",
              "width_policy": "fit",
              "height_policy": "fit",
              "z_index": 4,
              "properties": {
                "content": "Computes spacing, padding, and constraints.",
                "font_family": "Arial",
                "font_size": 18.0,
                "color": "#9CA3AF"
              }
            }
          ]
        }
      ]
    }
  ],
  "metadata": {
    "created_by": "Design Layout Engine Phase 2",
    "template": "Auto Layout Card",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Auto Layout Solver & Validator ===")
    try:
        layout = validate_layout(TEST_FLOW_LAYOUT)
        print("✓ Pydantic verified Stack Layout structure.")
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
        sys.exit(1)

    print("\n=== Solving Layout Constraints ===")
    try:
        renderer = CanvasRenderer()
        output_path = renderer.render(layout, filename="test_layout_flow.png")
        print(f"✓ Success! Auto Layout layout generated preview: {output_path}")
        
        # Verify coordinates resolved dynamically during pipeline
        card_group = layout.scene_tree[0]
        bg_panel = card_group.children[0]
        content_stack = card_group.children[1]
        
        title_text = content_stack.children[0]
        divider = content_stack.children[1]
        body_text = content_stack.children[2]
        
        print(f"Resolutions:")
        print(f"  Container size: {card_group.width}x{card_group.height}")
        print(f"  BG size: {bg_panel.width}x{bg_panel.height} (Stretches to 100%)")
        print(f"  Stack size: {content_stack.width}x{content_stack.height} (Stretches to 100%)")
        print(f"  Title pos inside stack: ({title_text.x:.1f}, {title_text.y:.1f})")
        print(f"  Divider size: {divider.width}x{divider.height} at y={divider.y:.1f}")
        print(f"  Body pos inside stack: ({body_text.x:.1f}, {body_text.y:.1f})")
        
        # Ensure sequential progression down the main vertical axis
        assert title_text.y < divider.y < body_text.y, "Auto Layout solver positioning sequence failed!"
        # Ensure children are inside the padding area (x >= padding_left)
        assert title_text.x >= content_stack.padding_left, "Padding constraint violation!"
        print("✓ Positioning geometry verification succeeded.")
        print("=== Complete Layout Engine Test Passed ===")
    except Exception as e:
        print(f"✗ Solving layout constraints crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
