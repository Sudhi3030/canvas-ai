import os
import sys
import json
from unittest.mock import MagicMock

# Ensure workspace root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.ai.prompt_builder import PromptBuilder, DesignRequirements
from design_engine.ai.gemini_provider import LLMServiceClient
from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

# Mock Layout JSON that simulates a successful response from OpenAI GPT-4o
MOCK_GPT_RESPONSE = {
  "canvas": {
    "width": 1080,
    "height": 1080,
    "background_color": "#3E2723",
    "unit": "px"
  },
  "elements": [
    {
      "id": "header_background",
      "name": "Header Accents",
      "type": "shape",
      "x": 0,
      "y": 0,
      "width": 1080,
      "height": 220,
      "rotation": 0.0,
      "z_index": 1,
      "opacity": 1.0,
      "properties": {
        "fill_color": "#4E342E",
        "border_radius": 0
      }
    },
    {
      "id": "title_text",
      "name": "Main Title",
      "type": "text",
      "x": 100,
      "y": 60,
      "width": 880,
      "height": 100,
      "rotation": 0.0,
      "z_index": 2,
      "opacity": 1.0,
      "properties": {
        "content": "Coffee House",
        "font_family": "Arial",
        "font_size": 64.0,
        "font_weight": "bold",
        "color": "#E0F2F1"
      }
    },
    {
      "id": "offer_text",
      "name": "Offer Highlight",
      "type": "text",
      "x": 100,
      "y": 400,
      "width": 880,
      "height": 150,
      "rotation": -4.0,
      "z_index": 3,
      "opacity": 1.0,
      "properties": {
        "content": "Buy 1 Get 1 Free!",
        "font_family": "Arial",
        "font_size": 72.0,
        "font_weight": "bold",
        "color": "#FFD54F"
      }
    },
    {
      "id": "cta_button",
      "name": "CTA Button",
      "type": "button",
      "x": 340,
      "y": 800,
      "width": 400,
      "height": 90,
      "rotation": 0.0,
      "z_index": 4,
      "opacity": 1.0,
      "properties": {
        "content": "Get Coupon Now",
        "font_family": "Arial",
        "font_size": 24.0,
        "font_weight": "bold",
        "text_color": "#3E2723",
        "fill_color": "#E0F2F1",
        "border_radius": 15
      }
    }
  ],
  "metadata": {
    "created_by": "Mock LLM Client",
    "template": "Warm Minimal Cafe Promo",
    "version": "1.0"
  }
}

def main():
    print("=== Running Mocked AI Generation Pipeline Test ===")
    
    # 1. Build Prompts
    print("\n[Step 1] Creating Design requirements & Building prompts...")
    builder = PromptBuilder()
    reqs = DesignRequirements(
        business_name="Coffee House",
        platform="Instagram",
        primary_color="#3E2723",
        offer="Buy 1 Get 1 Free!",
        cta="Get Coupon",
        business_type="Cafe Shop",
        theme="Warm Minimal",
        secondary_color="#E0F2F1"
    )
    sys_prompt = builder.build_system_prompt()
    user_prompt = builder.build_user_prompt(reqs)
    print("✓ Prompts built successfully.")

    # 2. Mock LLM Service Response
    print("\n[Step 2] Simulating LLM Generation (Mocking OpenAI API)...")
    llm_client = LLMServiceClient()
    # Replace the real network call with a mock returning our pre-defined valid JSON
    llm_client.generate_layout_json = MagicMock(return_value=json.dumps(MOCK_GPT_RESPONSE))
    
    raw_json = llm_client.generate_layout_json(sys_prompt, user_prompt)
    print("✓ Simulating OpenAI returned valid layout payload.")

    # 3. Pydantic Validation Check
    print("\n[Step 3] Parsing and Validating Layout JSON structure...")
    layout_obj = validate_layout(raw_json)
    print("✓ Structure validation succeeded. Pydantic parsed correct element types.")

    # 4. Save JSON Layout to disk
    json_dir = "outputs/json"
    os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, "mock_layout.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(MOCK_GPT_RESPONSE, f, indent=2)
    print(f"✓ Saved simulated JSON to: {json_path}")

    # 5. PNG Rendering Check
    print("\n[Step 4] Rasterizing Layout using Pillow Renderer...")
    renderer = CanvasRenderer()
    output_path = renderer.render(layout_obj, filename="mock_coffee_house.png")
    
    print(f"\n✓ Success! Preview rendered successfully.")
    print(f"✓ Output Image: {output_path}")
    print(f"✓ Output Layout JSON: {json_path}")
    assert os.path.exists(output_path), "Rendering error: PNG output was not written!"
    print("\n=== Mock Integration Test Completed Successfully ===")

if __name__ == "__main__":
    main()
