import os
import logging
from typing import Dict, Any

from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateEngine
from design_engine.renderer.canvas_renderer import CanvasRenderer
from design_engine.export.export_engine import ExportEngine
from design_engine.project_manager.storage import BaseProjectStorage, FileProjectStorage, StorageException

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s")
logger = logging.getLogger("PipelineOrchestrator")

def run_pipeline(
    business_name: str,
    platform: str,
    heading: str,
    body: str,
    primary_color: str,
    secondary_color: str,
    accent_color: str,
    logo_url: str = None,
    storage: BaseProjectStorage = None
) -> Dict[str, Any]:
    """
    Orchestrates the entire Creative Canvas AI design generator pipeline.
    Uses TemplateEngine, solves layouts, applies contrast rules, renders PNG previews,
    and exports printable PDF, WebP, and Fabric.js layered JSON files.
    """
    logger.info("Starting Branded Design Generation Pipeline...")
    
    if storage is None:
        storage = FileProjectStorage()

    # 1. Initialize Brand Identity
    logger.info("[1/5] Compiling brand kit properties...")
    brand = BrandKit(
        name=business_name,
        primary_color=primary_color,
        secondary_color=secondary_color,
        accent_color=accent_color,
        logo_url=logo_url
    )

    # 2. Build Semantic Scene Graph via AI Prompt Builder & Generation Pipeline
    logger.info("[2/5] Compiling semantic layout and querying AI model...")
    from design_engine.config import CONFIG
    from design_engine.ai.prompt_builder import PromptBuilder, DesignRequirements
    from design_engine.ai.gemini_provider import MockLLM, GeminiLLM, LLMServiceException
    from design_engine.semantic_scene.models import SemanticScene, SemanticNode
    from design_engine.variant_generator.generator import VariantGenerator
    from design_engine.layout_scorer.scorer import LayoutScorer
    from design_engine.design_optimizer.optimizer import DesignOptimizer

    # Check for Gemini API configurations
    if CONFIG.GEMINI_API_KEY:
        try:
            llm = GeminiLLM()
        except Exception:
            llm = MockLLM()
    else:
        llm = MockLLM()

    builder = PromptBuilder()
    reqs = DesignRequirements(
        business_name=business_name,
        platform=platform,
        primary_color=primary_color,
        offer=heading,
        cta="ORDER NOW",
        secondary_color=secondary_color,
        logo_available=bool(logo_url)
    )

    system_prompt = builder.build_system_prompt()
    user_prompt = builder.build_user_prompt(reqs)

    scene = None
    try:
        response_json = llm.generate_layout_json(system_prompt, user_prompt)
        scene = SemanticScene.model_validate_json(response_json)
        logger.info("Successfully compiled semantic scene graph from AI model.")
    except Exception as e:
        logger.warning(f"AI generation failed or skipped: {e}. Falling back to dynamic local semantic compilation.")
        
    if not scene:
        # Local compile fallback
        elements = []
        if logo_url:
            elements.append(SemanticNode(id="brand_logo", section="logo", role="logo_image", priority="medium", content=logo_url))
        if heading:
            elements.append(SemanticNode(id="header_text", section="hero", role="headline", priority="high", content=heading))
        if body:
            elements.append(SemanticNode(id="body_text", section="description", role="description", priority="medium", content=body))
        elements.append(SemanticNode(id="cta_button", section="cta", role="button", style="primary", priority="high", content="ORDER NOW"))
        scene = SemanticScene(elements=elements)
    
    # Generate the 5 variants
    generator = VariantGenerator()
    variants = generator.generate_variants(scene, platform, brand)
    
    optimizer = DesignOptimizer()
    scorer = LayoutScorer()
    
    best_layout = None
    best_score = -1.0
    
    for i, (theme, layout_variant) in enumerate(variants.items(), 1):
        # Optimize design rules (contrast, spacing, CTA visibility)
        optimizer.optimize(layout_variant)
        
        # Save intermediate variant debug file
        import os
        from design_engine.renderer.canvas_renderer import CanvasRenderer
        os.makedirs("outputs/variants", exist_ok=True)
        CanvasRenderer().render(layout_variant, f"../variants/variant_{i:02d}.png")
        
        # Score the resulting layout
        score = scorer.score(layout_variant)
        logger.info(f"Theme '{theme}' Layout Score: {score:.1f}/100.0")
        
        if score > best_score:
            best_score = score
            best_layout = layout_variant

    layout = best_layout

    # 3. Create Project Metadata Envelope
    logger.info("[3/5] Initializing filesystem storage envelope...")
    project_envelope = storage.create_project(business_name, platform, layout.model_dump())
    project_id = project_envelope["project_id"]

    try:
        # Save raw Scene Graph layout JSON
        storage.save_layout_json(project_id, project_envelope, overwrite=True)
        
        # 4. Solve Layout & Render Preview Image
        logger.info("[4/5] Solving layout constraints and rendering...")
        renderer = CanvasRenderer()
        rendered_image = renderer.render_to_image(layout)
        
        # Save preview image
        storage.save_rendered_image(project_id, rendered_image, overwrite=True)
        
        # 5. Export Multi-Formats (WebP, PDF, Layered JSON)
        logger.info("[5/5] Exporting PDF, WebP, and Fabric.js Layered JSON formats...")
        export_dir = os.path.join("outputs", "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        webp_path = os.path.join(export_dir, f"{project_id}.webp")
        pdf_path = os.path.join(export_dir, f"{project_id}.pdf")
        json_path = os.path.join(export_dir, f"{project_id}_layered.json")
        
        ExportEngine.export_raster(rendered_image, webp_path, "WEBP")
        ExportEngine.export_pdf(rendered_image, pdf_path)
        ExportEngine.export_layered_json(layout, json_path)
        
        logger.info("=== Pipeline Complete ===")
        return {
            "project_id": project_id,
            "layout_path": str(storage.json_dir / f"{project_id}.json"),
            "image_path": str(storage.image_dir / f"{project_id}.png"),
            "exports": {
                "webp": webp_path,
                "pdf": pdf_path,
                "layered_json": json_path
            },
            "status": "success"
        }
        
    except (StorageException, Exception) as e:
        logger.error(f"Pipeline failed: {e}")
        return {
            "project_id": project_id if "project_id" in locals() else None,
            "status": "failed",
            "error": str(e)
        }

if __name__ == "__main__":
    # Test Orchestrated generation using Salad Shop properties
    result = run_pipeline(
        business_name="Green Salad Shop",
        platform="Instagram",
        heading="FRESH SALADS DAILY",
        body="Organic greens, handmade dressings, and locally sourced ingredients. Order online now.",
        primary_color="#1E3A1E",      # Dark Green
        secondary_color="#2E7D32",    # Medium Green
        accent_color="#AEEA00",       # Lime Green Accent
        logo_url="https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80"
    )
    import pprint
    print("\nResult metadata returned:")
    pprint.pprint(result)