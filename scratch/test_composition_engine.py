import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.composition.engine import CompositionEngine
from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateSpec
from design_engine.semantic_scene.models import SemanticScene, SemanticNode
from design_engine.scene_graph.node import ImageNode, TextNode, ComponentNode

class TestCompositionEngine(unittest.TestCase):
    def test_composition_templates_building(self):
        scene = SemanticScene(elements=[
            SemanticNode(id="logo", section="logo", role="logo_image", priority="medium"),
            SemanticNode(id="heading", section="hero", role="headline", priority="high", content="Big Headline"),
            SemanticNode(id="body", section="description", role="description", priority="medium"),
            SemanticNode(id="hero", section="product", role="hero_image", priority="high"),
            SemanticNode(id="cta", section="cta", role="button", style="primary", priority="high")
        ])
        brand = BrandKit(name="Brand", primary_color="#000000", secondary_color="#FFFFFF")
        spec = TemplateSpec(name="Instagram Feed", width=800, height=800, padding=40, spacing=20, slots=[])
        
        engine = CompositionEngine()
        layouts = engine.build_all_compositions(scene, spec, brand)
        
        # Verify 10 distinct layouts are generated
        self.assertEqual(len(layouts), 10)
        
        # Verify Magazine contains overlay card z-index structure
        self.assertTrue(len(layouts["Magazine"].scene_tree) > 0)
        
        # Verify Hero Image occupies appropriate prominence in Centered Hero template
        hero_layout = layouts["Centered Hero"]
        
        # Find hero image and check proportions
        hero_node = None
        def traverse(node):
            nonlocal hero_node
            if isinstance(node, ImageNode) and node.id == "hero":
                hero_node = node
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)
                    
        for root in hero_layout.scene_tree:
            traverse(root)
            
        self.assertIsNotNone(hero_node)
        # Check that hero height occupies 40-60% of canvas height (800 * 0.45 = 360)
        self.assertTrue(320.0 <= hero_node.height <= 480.0)

if __name__ == "__main__":
    unittest.main()
