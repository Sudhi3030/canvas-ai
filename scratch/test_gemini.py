import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.ai.prompt_builder import PromptBuilder, DesignRequirements
from design_engine.ai.gemini_provider import GeminiLLM
from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer
from design_engine.project_manager.storage import FileProjectStorage

def main():
    print("=== Testing Live Google Gemini Layout Generation ===")
    
    # 1. Prepare inputs
    reqs = DesignRequirements(
        business_name="Green Salad Shop",
        platform="Instagram",
        primary_color="#2E7D32",
        offer="Fresh & Healthy 20% Off",
        cta="Order Delivery"
    )
    
    builder = PromptBuilder()
    sys_prompt = builder.build_system_prompt()
    user_prompt = builder.build_user_prompt(reqs)
    
    # 2. Call Gemini
    try:
        gemini_client = GeminiLLM()
        print("\nCalling Google Gemini API (gemini-1.5-flash)...")
        raw_json = gemini_client.generate_layout_json(sys_prompt, user_prompt)
        print("✓ Response obtained successfully.")
    except Exception as e:
        print(f"✗ Failed to connect or generate: {e}")
        sys.exit(1)
        
    # 3. Validate & Save
    try:
        layout = validate_layout(raw_json)
        print("✓ Layout JSON successfully validated via Pydantic.")
        
        storage = FileProjectStorage()
        project = storage.create_project("Green Salad", "Instagram", layout.model_dump())
        project_id = project["project_id"]
        
        storage.save_layout_json(project_id, project)
        
        renderer = CanvasRenderer()
        image = renderer.render_to_image(layout)
        image_path = storage.save_rendered_image(project_id, image)
        print(f"✓ Canvas rendered preview written to: {image_path}")
        print("=== Gemini Generation Test Completed Successfully ===")
    except Exception as e:
        print(f"✗ Post-generation parsing or rendering failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
