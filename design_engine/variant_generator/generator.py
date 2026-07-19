import copy
from typing import Dict
from design_engine.scene_graph.document import Layout
from design_engine.brand.brand_kit import BrandKit
from design_engine.template_slots.models import TemplateSlotRegistry
from design_engine.semantic_scene.models import SemanticScene
from design_engine.composition.engine import CompositionEngine
from design_engine.visual_styling.art_director import ArtDirector
from design_engine.visual_styling.visual_score import VisualScorer

class VariantGenerator:
    def generate_variants(self, scene: SemanticScene, template_name: str, brand: BrandKit) -> Dict[str, Layout]:
        """
        Generates 10 distinct design theme variants from the target semantic scene,
        applying 10 layout compositions and 5 visual styling profiles (50 candidates),
        and selecting the best visual combinations.
        """
        spec = TemplateSlotRegistry.get_template_spec(template_name)
        
        # 1. Build the 10 distinct composition layouts
        comp_engine = CompositionEngine()
        compositions = comp_engine.build_all_compositions(scene, spec, brand)
        
        styles = ["Minimal", "Modern", "Luxury", "Bold", "Elegant"]
        variants = {}
        
        for comp_name, base_layout in compositions.items():
            best_layout = None
            best_val_score = -1.0
            
            # Try 5 visual styles for each composition (50 candidates total)
            for style_name in styles:
                # Deep copy base layout state to prevent shared reference mutations
                layout_candidate = copy.deepcopy(base_layout)
                
                # Apply Art Direction styling
                ArtDirector.beautify(layout_candidate, style_name)
                
                # Re-solve coordinate positions post-styling
                from design_engine.layout_engine.layout import LayoutSolver
                LayoutSolver().solve(layout_candidate)
                
                # Audit visual aesthetic quality
                val_score = VisualScorer.evaluate_aesthetic_quality(layout_candidate)
                if val_score > best_val_score:
                    best_val_score = val_score
                    best_layout = layout_candidate
                    
            variants[comp_name] = best_layout
            
        return variants
