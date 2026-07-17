import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

TEST_COMPONENT_LAYOUT = {
  "canvas": {
    "width": 800,
    "height": 800,
    "background_color": "#0F172A",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "my_branded_button",
      "name": "Sign Up Button Component",
      "type": "component",
      "component_type": "button",
      "x": 250, "y": 350, "width": 300, "height": 70,
      "z_index": 1,
      "label": "CREATE ACCOUNT",
      "bg_color": "#10B981", # Emerald Green
      "text_color": "#FFFFFF",
      "border_radius": 32,
      "icon_url": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=50&q=80"
    }
  ],
  "metadata": {
    "created_by": "Component Engine Phase 2",
    "template": "Component Test",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Component Compilation & Validator ===")
    try:
        layout = validate_layout(TEST_COMPONENT_LAYOUT)
        print("✓ Pydantic validated and compiled layout.")
        
        # Verify children list was populated automatically
        comp_node = layout.scene_tree[0]
        assert len(comp_node.children) == 2, "Error: Children list was not auto-compiled!"
        assert comp_node.children[0].type == "shape", "Error: Background shape missing!"
        assert comp_node.children[1].type == "group", "Error: Horizontal aligner missing!"
        print("✓ Model validator compiled nested sub-components tree successfully.")
    except Exception as e:
        print(f"✗ Component validation failed: {e}")
        sys.exit(1)

    print("\n=== Rendering Component Banner Preview ===")
    try:
        renderer = CanvasRenderer()
        output_path = renderer.render(layout, filename="test_component_button.png")
        print(f"✓ Success! Branded component card written at: {output_path}")
        assert os.path.exists(output_path)
        print("=== Component Engine Test Passed ===")
    except Exception as e:
        print(f"✗ Rendering failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
