import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

# Typographic Poster layout JSON
TEST_TYPOGRAPHY_LAYOUT = {
  "canvas": {
    "width": 800,
    "height": 1000,
    "background_color": "#0F172A",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "poster_stack",
      "name": "Poster Layout Column",
      "type": "group",
      "x": 50,
      "y": 50,
      "width": 700,
      "height": 900,
      "layout_mode": "vertical",
      "spacing": 50.0,
      "padding_left": 40.0,
      "padding_right": 40.0,
      "padding_top": 60.0,
      "padding_bottom": 60.0,
      "cross_align": "stretch",  # Stretches elements across available 620px width
      "main_align": "center",
      "z_index": 1,
      "children": [
        {
          "id": "poster_title",
          "name": "Main Display Header",
          "type": "text",
          "width_policy": "fill",   # Takes full 620px width
          "height": 150.0,          # Explicit tall box to check vertical align center
          "z_index": 2,
          "properties": {
            "content": "CREATIVE CANVAS",
            "font_family": "Arial",
            "font_size": 56.0,
            "color": "#F8FAFC",
            "align": "center",
            "vertical_align": "middle",
            "letter_spacing": 4.0,   # Elegant title gaps
            "stroke_color": "#38BDF8",
            "stroke_width": 2,
            "shadow_color": "#020617",
            "shadow_offset_x": 4.0,
            "shadow_offset_y": 4.0
          }
        },
        {
          "id": "divider",
          "name": "Divider",
          "type": "shape",
          "width_policy": "fill",
          "height": 4.0,
          "properties": {
            "fill_color": "#38BDF8"
          }
        },
        {
          "id": "poster_body",
          "name": "Wrapped Body Text Block",
          "type": "text",
          "width_policy": "fill",
          "height_policy": "fit",    # Dynamic box height based on wrapping lines
          "z_index": 3,
          "properties": {
            "content": "The typography engine parses long paragraph sentences, wraps text words onto new lines when they exceed boundary limits, and applies custom line height parameters to maintain neat column rhythm.",
            "font_family": "Arial",
            "font_size": 24.0,
            "color": "#94A3B8",
            "align": "left",
            "line_height": 1.5      # Wide line heights for body text readability
          }
        },
        {
          "id": "poster_footer",
          "name": "Footer Metadata Tag",
          "type": "text",
          "width_policy": "fill",
          "height_policy": "fit",
          "z_index": 4,
          "properties": {
            "content": "DESIGN ENGINE V3.0",
            "font_family": "Arial",
            "font_size": 18.0,
            "color": "#64748B",
            "align": "right",
            "letter_spacing": 8.0   # Highly spaced metadata tag
          }
        }
      ]
    }
  ],
  "metadata": {
    "created_by": "Design Typography Engine Phase 3",
    "template": "Typography Poster Showcase",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Typography Engine Parser & Validator ===")
    try:
        layout = validate_layout(TEST_TYPOGRAPHY_LAYOUT)
        print("✓ Pydantic verified Typography properties.")
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
        sys.exit(1)

    print("\n=== Rendering Typography Showcase ===")
    try:
        renderer = CanvasRenderer()
        output_path = renderer.render(layout, filename="test_typography.png")
        print(f"✓ Success! Typographic layout rendered preview: {output_path}")
        assert os.path.exists(output_path), "Error: Preview image not found!"
        print("=== Typography Engine Test Passed ===")
    except Exception as e:
        print(f"✗ Typographic solver/renderer failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
