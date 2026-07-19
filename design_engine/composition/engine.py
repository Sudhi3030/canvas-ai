from typing import Dict, Optional
from design_engine.scene_graph.document import Layout
from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateSpec
from design_engine.semantic_scene.models import SemanticScene

# Import templates
from design_engine.composition.templates.hero import HeroTemplate
from design_engine.composition.templates.split import SplitTemplate
from design_engine.composition.templates.overlay import OverlayTemplate
from design_engine.composition.templates.magazine import MagazineTemplate
from design_engine.composition.templates.editorial import EditorialTemplate
from design_engine.composition.templates.poster import PosterTemplate
from design_engine.composition.templates.bento import BentoTemplate
from design_engine.composition.templates.minimal import MinimalTemplate
from design_engine.composition.templates.story import StoryTemplate
from design_engine.composition.templates.card import CardTemplate

class CompositionEngine:
    def build_all_compositions(
        self,
        scene: SemanticScene,
        spec: TemplateSpec,
        brand: BrandKit
    ) -> Dict[str, Layout]:
        """
        Builds 10 fundamentally distinct Layout documents from the same semantic scene.
        """
        # Resolve slot values with default fallbacks
        logo = brand.logo_url or "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80"
        heading = "Headline Text"
        body = "Description copy goes here."
        cta = "ORDER NOW"
        hero_url = "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&q=80"
        
        for node in scene.elements:
            if node.role == "logo_image" or node.section == "logo":
                logo = node.content or logo
            elif node.role == "headline" or node.section == "hero":
                heading = node.content or heading
            elif node.role == "description" or node.section == "description":
                body = node.content or body
            elif node.role == "button" or node.section == "cta":
                cta = node.content or cta
            elif node.role == "hero_image" or node.section == "product":
                hero_url = node.content or hero_url
                
        return {
            "Centered Hero": HeroTemplate.build(spec, brand, logo, heading, body, cta, hero_url),
            "Split Layout": SplitTemplate.build(spec, brand, logo, heading, body, cta, hero_url),
            "Editorial": EditorialTemplate.build(spec, brand, logo, heading, body, cta, hero_url),
            "Magazine": MagazineTemplate.build(spec, brand, logo, heading, body, cta, hero_url),
            "Minimal": MinimalTemplate.build(spec, brand, logo, heading, body, cta, hero_url),
            "Premium": CardTemplate.build(spec, brand, logo, heading, body, cta, hero_url),
            "Bento Grid": BentoTemplate.build(spec, brand, logo, heading, body, cta, hero_url),
            "Glass Card": OverlayTemplate.build(spec, brand, logo, heading, body, cta, hero_url),
            "Image Focus": StoryTemplate.build(spec, brand, logo, heading, body, cta, hero_url),
            "Typography Focus": PosterTemplate.build(spec, brand, logo, heading, body, cta, hero_url)
        }
