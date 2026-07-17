import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer
from design_engine.export.export_engine import ExportEngine

# Card layout with animation tags
TEST_EXPORT_LAYOUT = {
  "canvas": {
    "width": 800,
    "height": 800,
    "background_color": "#0F172A",
    "unit": "px"
  },
  "scene_tree": [
    {
      "id": "container_group",
      "name": "Animated Container Group",
      "type": "group",
      "x": 150, "y": 150, "width": 500, "height": 500,
      "layout_mode": "vertical",
      "spacing": 30.0,
      "padding_left": 40.0,
      "padding_top": 40.0,
      "z_index": 1,
      "children": [
        {
          "id": "card_bg",
          "name": "Panel Shape",
          "type": "shape",
          "width_policy": "fill", "height_policy": "fill",
          "z_index": 1,
          "animation": {
            "effect": "fade",
            "duration": 1.5,
            "delay": 0.0
          },
          "properties": {
            "fill_color": "#1E293B",
            "border_radius": 16
          }
        },
        {
          "id": "card_title",
          "name": "Header Text",
          "type": "text",
          "width_policy": "fit", "height_policy": "fit",
          "z_index": 2,
          "animation": {
            "effect": "slide_in",
            "duration": 1.0,
            "delay": 0.5
          },
          "properties": {
            "content": "Animated Export Card",
            "font_family": "Arial",
            "font_size": 36.0,
            "color": "#38BDF8"
          }
        }
      ]
    }
  ],
  "metadata": {
    "created_by": "Export Engine Phase 7",
    "template": "Export Showcase",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Exporter & Animation Engine ===")
    
    # 1. Parse and validate layout
    try:
        layout = validate_layout(TEST_EXPORT_LAYOUT)
        print("✓ Pydantic verified animation metadata schema.")
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        sys.exit(1)

    # 2. Render base canvas
    renderer = CanvasRenderer()
    base_img = renderer.render_to_image(layout)
    
    # 3. Export formats
    print("\nRunning exports pipeline...")
    try:
        # A. WebP export
        webp_path = "outputs/exports/test_card.webp"
        ExportEngine.export_raster(base_img, webp_path, "WEBP")
        print(f"✓ Modern WebP image exported: {webp_path}")
        assert os.path.exists(webp_path)

        # B. PDF export
        pdf_path = "outputs/exports/test_card.pdf"
        ExportEngine.export_pdf(base_img, pdf_path)
        print(f"✓ High-fidelity PDF document exported: {pdf_path}")
        assert os.path.exists(pdf_path)

        # C. Layered JSON export
        json_path = "outputs/exports/test_layered.json"
        ExportEngine.export_layered_json(layout, json_path)
        print(f"✓ Solved Layered JSON document exported: {json_path}")
        assert os.path.exists(json_path)

        # D. Validate Layered JSON values
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        assert data["canvas"]["width"] == 800
        # Check coordinates resolved to absolute values (e.g. title text is positioned inside padding)
        layers = data["layers"]
        assert len(layers) == 2
        bg_layer = layers[0]
        title_layer = layers[1]
        
        print(f"\nSolved Absolute Positions in Layered JSON:")
        print(f"  Canvas size: {data['canvas']['width']}x{data['canvas']['height']}")
        print(f"  Layer '{bg_layer['name']}': left={bg_layer['left']:.1f}, top={bg_layer['top']:.1f}")
        print(f"  Layer '{title_layer['name']}': left={title_layer['left']:.1f}, top={title_layer['top']:.1f}")
        
        # Assert animations are parsed
        assert title_layer["animation"]["effect"] == "slide_in"
        assert title_layer["animation"]["duration"] == 1.0
        print("✓ Layered JSON animations metadata verified.")
        print("=== Export Engine Test Passed ===")
    except Exception as e:
        print(f"✗ Exporter pipeline execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
