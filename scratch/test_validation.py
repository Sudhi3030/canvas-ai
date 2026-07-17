import json
import os
import sys
from pydantic import ValidationError

# Ensure workspace root is in path to import models and validator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout, format_validation_error, generate_layout_schema
from design_engine.scene_graph.node import TextElement, Layout

# 1. Sample valid JSON structure provided by the user
VALID_LAYOUT_JSON = {
  "canvas": {
    "width": 1080,
    "height": 1080,
    "background_color": "#FFFFFF",
    "unit": "px"
  },
  "elements": [
    {
      "id": "text_1",
      "name": "Main Heading",
      "type": "text",
      "x": 120,
      "y": 80,
      "width": 700,
      "height": 120,
      "rotation": 0,
      "z_index": 1,
      "opacity": 1.0,
      "visible": True,
      "locked": False,
      "selectable": True,
      "properties": {
        "content": "50% OFF",
        "font_family": "Poppins",
        "font_size": 72,
        "font_weight": "bold",
        "color": "#FFFFFF"
      }
    }
  ],
  "metadata": {
    "created_by": "Creative Canvas AI",
    "template": "Instagram Sale",
    "version": "1.0"
  }
}

# 2. Sample invalid JSON structures for testing validation bounds
INVALID_BACKGROUND_COLOR = {
    **VALID_LAYOUT_JSON,
    "canvas": {
        "width": 1080,
        "height": 1080,
        "background_color": "not-a-color",
        "unit": "px"
    }
}

INVALID_ELEMENT_DIMENSIONS = {
    **VALID_LAYOUT_JSON,
    "elements": [
        {
            "id": "text_1",
            "name": "Main Heading",
            "type": "text",
            "x": 120,
            "y": 80,
            "width": -100,  # Invalid: must be > 0
            "height": 120,
            "properties": {
                "content": "50% OFF",
                "font_size": 72,
                "color": "#FFFFFF"
            }
        }
    ]
}

INVALID_DISCRIMINATOR = {
    **VALID_LAYOUT_JSON,
    "elements": [
        {
            "id": "item_1",
            "name": "Unknown Layer",
            "type": "unknown_type",  # Invalid type discriminator
            "x": 120,
            "y": 80,
            "width": 100,
            "height": 100,
            "properties": {}
        }
    ]
}

def test_validation():
    print("=== Running Layout Schema Validation Tests ===")

    # Test 1: Valid Layout validation
    print("\n[Test 1] Validating standard layout JSON...")
    try:
        layout = validate_layout(VALID_LAYOUT_JSON)
        print("✓ Success! Layout parsed and validated successfully.")
        
        # Verify content typing
        assert len(layout.elements) == 1
        element = layout.elements[0]
        assert isinstance(element, TextElement)
        assert element.properties.content == "50% OFF"
        assert element.properties.font_size == 72.0
        print("✓ Checked element type constraints and nested values.")
    except Exception as e:
        print(f"✗ Failed to validate layout: {e}")
        sys.exit(1)

    # Test 2: Invalid Background Color
    print("\n[Test 2] Validating error for invalid background color...")
    try:
        validate_layout(INVALID_BACKGROUND_COLOR)
        print("✗ Failed: Expected validation error for background color format but none raised.")
        sys.exit(1)
    except ValidationError as e:
        print("✓ Success! Caught expected ValidationError.")
        error_msg = format_validation_error(e)
        print(error_msg)
        assert "background_color" in error_msg

    # Test 3: Invalid Element Dimensions
    print("\n[Test 3] Validating error for negative dimensions...")
    try:
        validate_layout(INVALID_ELEMENT_DIMENSIONS)
        print("✗ Failed: Expected validation error for negative element width but none raised.")
        sys.exit(1)
    except ValidationError as e:
        print("✓ Success! Caught expected ValidationError.")
        error_msg = format_validation_error(e)
        print(error_msg)
        assert "width" in error_msg

    # Test 4: Invalid Discriminator Type
    print("\n[Test 4] Validating error for unknown element types...")
    try:
        validate_layout(INVALID_DISCRIMINATOR)
        print("✗ Failed: Expected validation error for invalid discriminator 'type' but none raised.")
        sys.exit(1)
    except ValidationError as e:
        print("✓ Success! Caught expected ValidationError.")
        error_msg = format_validation_error(e)
        print(error_msg)
        assert "type" in error_msg

    # Export Schema to schema/layout_schema.json
    print("\n[Export] Generating JSON schema and writing to file...")
    try:
        schema = generate_layout_schema()
        schema_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "schema"))
        os.makedirs(schema_dir, exist_ok=True)
        schema_path = os.path.join(schema_dir, "layout_schema.json")
        
        with open(schema_path, "w") as f:
            json.dump(schema, f, indent=2)
        print(f"✓ Success! Schema exported to {schema_path}")
    except Exception as e:
        print(f"✗ Failed to export schema: {e}")
        sys.exit(1)

    print("\n=== All Tests Passed Successfully ===")

if __name__ == "__main__":
    test_validation()
