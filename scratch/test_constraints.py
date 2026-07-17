import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

# Deliberately flawed layout payload
BAD_LAYOUT = {
  "canvas": {
    "width": 1000,
    "height": 1000,
    "background_color": "#0F172A",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "bad_panel",
      "name": "Dark Blue Background Shape",
      "type": "shape",
      "x": 100, "y": 100, "width": 800, "height": 800,
      "z_index": 1,
      "properties": {
        "fill_color": "#1E3A8A"  # Dark Blue
      }
    },
    {
      "id": "low_contrast_text",
      "name": "Low Contrast Title Text",
      "type": "text",
      "x": 200, "y": 150, "width": 600, "height": 80,
      "z_index": 2,
      "properties": {
        "content": "BAD CONTRAST TEXT",
        "font_family": "Arial",
        "font_size": 36.0,
        "color": "#1E293B"  # Almost matching dark grey-blue (Contrast ~ 1.2:1)
      }
    },
    {
      "id": "overflow_text_box",
      "name": "Overflow Text Block",
      "type": "text",
      "x": 200, "y": 300, "width": 600, "height": 80, # Tall font 56pt in an 80px high box!
      "height_policy": "fixed",
      "z_index": 3,
      "properties": {
        "content": "This giant sentence will overflow a fixed text box and trigger auto-shrink rules.",
        "font_family": "Arial",
        "font_size": 48.0,
        "color": "#FFFFFF"
      }
    },
    {
      "id": "escaping_shape",
      "name": "Outside Canvas Panel",
      "type": "shape",
      "x": 950, "y": 950, "width": 200, "height": 200, # Escapes boundary bottom-right
      "z_index": 4,
      "properties": {
        "fill_color": "#EF4444"
      }
    }
  ],
  "metadata": {
    "created_by": "Design Rules Engine Phase 5",
    "template": "Rules Test Layout",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Constraint & Design Rules Solver ===")
    try:
        layout = validate_layout(BAD_LAYOUT)
        print("✓ Pydantic verified test layout schema.")
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        sys.exit(1)

    print("\n=== Rendering and Applying Auto-Fixes ===")
    try:
        # Before corrections check
        orig_text = layout.scene_tree[1]
        orig_overflow = layout.scene_tree[2]
        orig_escape = layout.scene_tree[3]
        
        print("Initial States:")
        print(f"  Title Color: {orig_text.properties.color}")
        print(f"  Overflow Font Size: {orig_overflow.properties.font_size}pt")
        print(f"  Escaping Node x/y: ({orig_escape.x}, {orig_escape.y})")
        
        # Render triggers solve + rules corrections
        renderer = CanvasRenderer()
        output_path = renderer.render(layout, filename="test_constraints_fixed.png")
        print(f"\n✓ Success! Fixed preview rendered at: {output_path}")
        
        print("\nCorrected States:")
        print(f"  Title Color: {orig_text.properties.color} (Expected #FFFFFF contrast fix)")
        print(f"  Overflow Font Size: {orig_overflow.properties.font_size:.1f}pt (Expected auto-shrunk size)")
        print(f"  Escaping Node x/y: ({orig_escape.x:.1f}, {orig_escape.y:.1f}) (Expected clamped coordinates)")
        
        # Asserts
        assert orig_text.properties.color == "#FFFFFF", "Contrast Auto-fix failed!"
        assert orig_overflow.properties.font_size < 48.0, "Font-size Auto-shrink failed!"
        assert orig_escape.x + orig_escape.width <= 1000.0, "Right boundary clamp failed!"
        assert orig_escape.y + orig_escape.height <= 1000.0, "Bottom boundary clamp failed!"
        
        print("\n✓ All assertions passed successfully. Engine repaired layout faults.")
        print("=== Complete Constraint Engine Test Passed ===")
    except Exception as e:
        print(f"✗ Constraint engine logic failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
