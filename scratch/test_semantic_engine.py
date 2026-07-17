import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.semantic_scene.models import SemanticScene, SemanticNode
from design_engine.variant_generator.generator import VariantGenerator
from design_engine.layout_scorer.scorer import LayoutScorer
from design_engine.brand.brand_kit import BrandKit
from design_engine.renderer.canvas_renderer import CanvasRenderer

TEST_SCENE = SemanticScene(
    elements=[
        SemanticNode(id="logo", section="logo", role="logo_image", priority="medium", content="https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80"),
        SemanticNode(id="head", section="hero", role="headline", priority="high", content="ORGANIC & FRESH"),
        SemanticNode(id="body", section="description", role="description", priority="medium", content="Healthy salads delivered directly to your doorstep. Clean eating made easy."),
        SemanticNode(id="cta", section="cta", role="button", style="primary", priority="high", content="ORDER NOW")
    ]
)

def main():
    print("=== Testing Semantic Layout Engine ===")
    brand = BrandKit(
        name="Healthy Food",
        primary_color="#1E3D29",
        secondary_color="#14261C",
        accent_color="#8FDF74",
        font_heading="Arial",
        font_body="Arial"
    )
    
    generator = VariantGenerator()
    variants = generator.generate_variants(TEST_SCENE, "Instagram", brand)
    
    scorer = LayoutScorer()
    
    print("\nScoring generated design variants:")
    best_variant = None
    best_score = -1.0
    
    for theme, layout in variants.items():
        score = scorer.score(layout)
        print(f"- Variant {theme}: Score = {score:.1f}/100.0")
        if score > best_score:
            best_score = score
            best_variant = (theme, layout)
            
    print(f"\nSelected Best Variant: {best_variant[0]} (Score: {best_score:.1f})")
    
    renderer = CanvasRenderer()
    output_path = renderer.render(best_variant[1], filename=f"test_semantic_{best_variant[0].lower()}.png")
    print(f"✓ Success! Rendered best variant at: {output_path}")
    assert os.path.exists(output_path)
    
    # Assertions
    assert len(variants) == 5, "Should generate exactly 5 variants"
    assert best_score >= 0.0, "Score should be valid"
    
    print("=== Semantic Engine Tests Passed ===")

if __name__ == "__main__":
    main()
