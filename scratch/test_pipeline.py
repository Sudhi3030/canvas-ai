import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.ai.prompt_builder import PromptBuilder, DesignRequirements
from design_engine.ai.gemini_provider import LLMServiceClient
from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

def main():
    print("=== Testing AI Design Pipeline Components ===")
    
    # 1. Initialize prompts
    print("\n[Step 1] Building design prompts...")
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
    
    print("✓ System Prompt generated successfully (Length:", len(sys_prompt), ")")
    print("✓ User Prompt generated successfully:\n", user_prompt)

    # 2. Call OpenAI Service
    print("\n[Step 2] Contacting OpenAI service...")
    try:
        client = LLMServiceClient()
        raw_json = client.generate_layout_json(sys_prompt, user_prompt)
        print("✓ Response obtained. Content details:\n", raw_json)
    except Exception as e:
        print(f"✗ Network or service failure during LLM connection: {e}")
        print("Ensure valid OPENAI_API_KEY environment variable is configured.")
        sys.exit(1)

    # 3. Parse and Validate Pydantic Models
    print("\n[Step 3] Parsing and Validating Layout JSON...")
    try:
        layout_obj = validate_layout(raw_json)
        print("✓ Pydantic validation successful.")
    except Exception as e:
        print(f"✗ Validation failure: {e}")
        sys.exit(1)

    # 4. Canvas rendering check
    print("\n[Step 4] Rendering output preview...")
    try:
        renderer = CanvasRenderer()
        output_path = renderer.render(layout_obj, filename="coffee_house_promo.png")
        print(f"✓ Success! Image generated at: {output_path}")
        assert os.path.exists(output_path), "Error: Output PNG file does not exist!"
        print("=== Complete Pipeline Test Passed ===")
    except Exception as e:
        print(f"✗ Rendering failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
