import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.visual_styling.art_director import ArtDirector
from design_engine.variant_generator.generator import VariantGenerator
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import TextNode, ComponentNode
from design_engine.semantic_scene.models import SemanticScene, SemanticNode
from design_engine.brand.brand_kit import BrandKit

class TestVisualArtDirection(unittest.TestCase):
    def test_art_direction_beautify(self):
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[
                TextNode(
                    id="header_text", name="Heading",
                    x=50, y=50, width=400, height=80,
                    properties={"content": "Headline copy", "color": "#000000", "font_size": 24.0}
                )
            ],
            metadata=Metadata()
        )
        
        ArtDirector.beautify(layout, "Luxury")
        
        # Verify serif font (Georgia) was selected for Luxury
        node = layout.scene_tree[1] # Injected accent background decoration at index 0
        self.assertEqual(node.properties.font_family, "Georgia")

    def test_variant_multiplexing(self):
        scene = SemanticScene(elements=[
            SemanticNode(id="logo", section="logo", role="logo_image", priority="medium"),
            SemanticNode(id="heading", section="hero", role="headline", priority="high", content="Headline Text"),
            SemanticNode(id="body", section="description", role="description", priority="medium"),
            SemanticNode(id="hero", section="product", role="hero_image", priority="high"),
            SemanticNode(id="cta", section="cta", role="button", style="primary", priority="high")
        ])
        brand = BrandKit(name="Brand", primary_color="#000000", secondary_color="#FFFFFF")
        
        generator = VariantGenerator()
        variants = generator.generate_variants(scene, "Instagram Feed", brand)
        
        # Verify 10 distinct composition strategies are generated
        self.assertEqual(len(variants), 10)
        
        # Verify bounding box variance across strategies
        keys = list(variants.keys())
        first_layout = variants[keys[0]]
        second_layout = variants[keys[1]]
        
        # Check that they represent unique compositions
        self.assertNotEqual(
            first_layout.scene_tree[1].children[1].layout_mode,
            second_layout.scene_tree[1].children[1].layout_mode
        )

if __name__ == "__main__":
    unittest.main()
