import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

TEST_SCENE_GRAPH = {
  "canvas": {
    "width": 1000,
    "height": 1000,
    "background_color": "#F3F4F6",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "root_heading",
      "name": "Header Title",
      "type": "text",
      "x": 100,
      "y": 100,
      "width": 800,
      "height": 80,
      "rotation": 0.0,
      "z_index": 3,
      "opacity": 1.0,
      "visible": True,
      "locked": False,
      "properties": {
        "content": "Scene Graph Document Engine",
        "font_family": "Arial",
        "font_size": 42.0,
        "color": "#1F2937"
      }
    },
    {
      "id": "container_group",
      "name": "Main Feature Group",
      "type": "group",
      "x": 200,
      "y": 300,
      "width": 600,
      "height": 500,
      "rotation": 10.0,  # Rotates the whole group context
      "z_index": 1,
      "opacity": 0.8,    # Fades group and all nested children
      "visible": True,
      "locked": False,
      "children": [
        {
          "id": "group_bg",
          "name": "Group Background Panel",
          "type": "shape",
          "x": 0,          # Local offset 0 relative to group top-left
          "y": 0,
          "width": 600,
          "height": 500,
          "rotation": 0.0,
          "z_index": 1,
          "opacity": 1.0,
          "visible": True,
          "locked": False,
          "properties": {
            "fill_color": "#3B82F6",
            "border_radius": 24
          }
        },
        {
          "id": "group_text",
          "name": "Group Inner Text",
          "type": "text",
          "x": 50,         # Local offset (50, 200) inside the blue panel
          "y": 200,
          "width": 500,
          "height": 100,
          "rotation": -10.0, # Rotates back relative to parent context
          "z_index": 2,
          "opacity": 1.0,
          "visible": True,
          "locked": False,
          "properties": {
            "content": "Nested Local Element",
            "font_family": "Arial",
            "font_size": 36.0,
            "color": "#FFFFFF"
          }
        }
      ]
    }
  ],
  "metadata": {
    "created_by": "Scene Graph Engine Phase 1",
    "template": "SaaS Showcase Template",
    "version": "2.0"
  }
}

def main():
    print("=== Testing Scene Graph Parser & Validator ===")
    try:
        layout = validate_layout(TEST_SCENE_GRAPH)
        print("✓ Pydantic verified Scene Graph Layout.")
        
        # Check recursive group nesting
        assert len(layout.scene_tree) == 2
        group = layout.scene_tree[1]
        assert group.type == "group"
        assert len(group.children) == 2
        print("✓ Scene tree structural recursion verified.")
    except Exception as e:
        print(f"✗ Failed structural validation: {e}")
        sys.exit(1)

    print("\n=== Testing Recursive Rendering Loop ===")
    try:
        renderer = CanvasRenderer()
        output_path = renderer.render(layout, filename="test_scene_graph.png")
        print(f"✓ Success! Scene graph preview rendered at: {output_path}")
        assert os.path.exists(output_path), "Error: Preview image not found!"
        print("=== Complete Scene Graph Test Passed ===")
    except Exception as e:
        print(f"✗ Failed rendering scene graph: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
