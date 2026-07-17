import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.design_rules.accessibility import DesignRulesEngine

BROKEN_LAYOUT = {
  "canvas": {
    "width": 800, "height": 800,
    "background_color": "#FFFFFF",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "header_text",
      "name": "Small Header Title",
      "type": "text",
      "x": 200, "y": 100, "width": 400, "height": 50,
      "properties": {
        "content": "LITTLE TITLE",
        "font_family": "Arial",
        "font_size": 14.0, # Smaller than body!
        "color": "#000000"
      }
    },
    {
      "id": "body_copy",
      "name": "Large Body Copy",
      "type": "text",
      "x": 200, "y": 200, "width": 400, "height": 100,
      "properties": {
        "content": "This body text is huge but has bad contrast.",
        "font_family": "Arial",
        "font_size": 24.0,
        "color": "#E2E8F0" # Almost invisible contrast!
      }
    },
    {
      "id": "tiny_copy",
      "name": "Tiny Legal Copy",
      "type": "text",
      "x": 200, "y": 400, "width": 400, "height": 40,
      "properties": {
        "content": "Tiny copy that is illegible.",
        "font_family": "Arial",
        "font_size": 8.0 # Too tiny!
      }
    },
    {
      "id": "cta_button",
      "name": "Hidden CTA Button",
      "type": "component",
      "component_type": "button",
      "x": 250, "y": 600, "width": 300, "height": 60,
      "visible": False, # Hidden CTA!
      "label": "CLICK ME",
      "bg_color": "#FFC107",
      "text_color": "#000000"
    }
  ],
  "metadata": {
    "created_by": "Design Validation Rules Test",
    "template": "Broken Test",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Design Rules Validator & Repairs ===")
    layout = validate_layout(BROKEN_LAYOUT)
    
    engine = DesignRulesEngine()
    warnings = engine.analyze_and_fix(layout)
    
    print("\nWarnings resolved and auto-repaired:")
    for w in warnings:
        print(f"- {w}")
        
    # Verify fixes
    header_node = layout.scene_tree[0]
    body_node = layout.scene_tree[1]
    tiny_node = layout.scene_tree[2]
    cta_node = layout.scene_tree[3]
    
    assert header_node.properties.font_size >= body_node.properties.font_size, "Error: Typographic hierarchy not corrected!"
    assert body_node.properties.color != "#E2E8F0", "Error: Low contrast color not adjusted!"
    assert tiny_node.properties.font_size >= 12.0, "Error: Tiny legible font size not corrected!"
    assert cta_node.visible == True, "Error: Hidden CTA button visible parameter not restored!"
    assert cta_node.opacity == 1.0, "Error: Hidden CTA button opacity not restored!"
    
    print("\n✓ Success! All design rule issues were automatically resolved.")

if __name__ == "__main__":
    main()
