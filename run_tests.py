import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from design_engine.scene_graph.node import TextNode, ShapeNode, GroupNode, ComponentNode, ShadowEffect, GlowEffect, BlurEffect
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.layout_engine.layout import LayoutSolver, wrap_text
from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateEngine
from design_engine.design_rules.accessibility import DesignRulesEngine
from design_engine.renderer.canvas_renderer import CanvasRenderer, load_font

class TestSceneGraph(unittest.TestCase):
    def test_node_validation(self):
        node = ShapeNode(
            id="test_rect",
            name="Test Rectangle Shape",
            x=10, y=20, width=150, height=250,
            properties={"fill_color": "#FF5722", "border_radius": 8}
        )
        self.assertEqual(node.properties.fill_color, "#FF5722")
        self.assertEqual(node.properties.border_radius, 8)
        self.assertEqual(node.x, 10.0)

class TestLayoutEngine(unittest.TestCase):
    def test_vertical_flow(self):
        c1 = ShapeNode(id="c1", name="Child 1", width=100, height=50, properties={})
        c2 = ShapeNode(id="c2", name="Child 2", width=100, height=60, properties={})
        
        group = GroupNode(
            id="v_stack", name="Vertical Stack Layout",
            width=200, height=400,
            layout_mode="vertical", spacing=15,
            padding_top=10, padding_bottom=10,
            children=[c1, c2]
        )
        
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[group],
            metadata=Metadata()
        )
        
        solver = LayoutSolver()
        solver.solve(layout)
        
        # Verify vertical stack math: y coordinates should stack sequentially
        # c1 y = padding_top (10.0)
        # c2 y = c1.y + c1.height (50.0) + spacing (15.0) = 75.0
        self.assertEqual(c1.y, 10.0)
        self.assertEqual(c2.y, 75.0)

class TestEffectsEngine(unittest.TestCase):
    def test_effects_parsing(self):
        node = ShapeNode(
            id="effects_node", name="Effects Card",
            effects=[
                ShadowEffect(type="drop_shadow", color="#000000", offset_x=0.0, offset_y=10.0, blur=20.0),
                GlowEffect(type="glow", color="#FF5722", blur=10.0),
                BlurEffect(type="blur", radius=5.0)
            ],
            properties={}
        )
        self.assertEqual(len(node.effects), 3)
        self.assertEqual(node.effects[0].type, "drop_shadow")
        self.assertEqual(node.effects[1].type, "glow")
        self.assertEqual(node.effects[2].type, "blur")

class TestComponentSystem(unittest.TestCase):
    def test_button_compiles(self):
        btn = ComponentNode(
            id="submit_button", name="Submit Button",
            type="component", component_type="button",
            width=200, height=50,
            label="SUBMIT", bg_color="#3F51B5", text_color="#FFFFFF"
        )
        # Verify that model validator dynamic compilation populated internal sub-components
        self.assertEqual(len(btn.children), 2)
        self.assertEqual(btn.children[0].type, "shape")
        self.assertEqual(btn.children[1].type, "group")

class TestTypography(unittest.TestCase):
    def test_wrap_boundaries(self):
        font = load_font("Arial", 16.0)
        text = "This is a longer line of text that needs to wrap inside bounds."
        lines = wrap_text(text, font, 200.0, 0.0)
        # Verify text was split into multiple lines
        self.assertTrue(len(lines) > 1)

class TestTemplates(unittest.TestCase):
    def test_slot_compilations(self):
        brand = BrandKit(
            name="Acme", 
            primary_color="#111111", 
            secondary_color="#222222", 
            accent_color="#333333",
            logo_url="https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80"
        )
        layout = TemplateEngine.create_branded_layout("Instagram", brand, "Title", "Body")
        
        # Verify main container contains slots
        main_container = layout.scene_tree[0]
        content_stack = main_container.children[1]
        children_ids = [child.id for child in content_stack.children]
        
        self.assertIn("brand_logo", children_ids)
        self.assertIn("header_text", children_ids)
        self.assertIn("body_text", children_ids)
        self.assertIn("cta_button", children_ids)

class TestDesignValidation(unittest.TestCase):
    def test_design_repairs(self):
        # Broken contrast + tiny font size + hidden CTA
        layout = Layout(
            canvas=Canvas(width=800, height=800, background_color="#FFFFFF"),
            scene_tree=[
                TextNode(
                    id="header_text", name="Small Header Title",
                    properties={"content": "LITTLE TITLE", "font_size": 14.0}
                ),
                TextNode(
                    id="body_copy", name="Legibility Text",
                    properties={"content": "Body Copy", "font_size": 8.0, "color": "#EEEEEE"} # Low contrast!
                ),
                ComponentNode(
                    id="cta_btn", name="Hidden CTA",
                    type="component", component_type="button",
                    visible=False # Hidden CTA!
                )
            ],
            metadata=Metadata()
        )
        
        engine = DesignRulesEngine()
        warnings = engine.analyze_and_fix(layout)
        
        # Verify repaired targets
        header = layout.scene_tree[0]
        body = layout.scene_tree[1]
        cta = layout.scene_tree[2]
        
        # Contrast & tiny size fixed
        self.assertEqual(body.properties.font_size, 12.0)
        self.assertNotEqual(body.properties.color, "#EEEEEE")
        # Hidden CTA restored
        self.assertTrue(cta.visible)
        self.assertEqual(cta.opacity, 1.0)
        # Hierarchy balanced: Header size must exceed body (12.0) * 1.5 = 18.0
        self.assertEqual(header.properties.font_size, 18.0)

class TestBrandKit(unittest.TestCase):
    def test_presets_inheritances(self):
        brand = BrandKit(name="Apple")
        # Verify defaults populated correctly
        self.assertIsNotNone(brand.shadow_preset)
        self.assertIsNotNone(brand.gradient_preset)
        self.assertEqual(brand.spacing_scale, 1.0)
        self.assertEqual(brand.button_radius, 24)

class TestSemanticAI(unittest.TestCase):
    def test_semantic_models(self):
        from design_engine.semantic_scene.models import SemanticNode, SemanticScene
        node = SemanticNode(id="node_1", section="hero", role="headline", content="Hello")
        self.assertEqual(node.id, "node_1")
        self.assertEqual(node.section, "hero")
        
    def test_variant_generation_and_scoring(self):
        from design_engine.semantic_scene.models import SemanticScene, SemanticNode
        from design_engine.variant_generator.generator import VariantGenerator
        from design_engine.layout_scorer.scorer import LayoutScorer
        
        scene = SemanticScene(
            elements=[
                SemanticNode(id="l1", section="logo", role="logo_image", content="logo_url"),
                SemanticNode(id="h1", section="hero", role="headline", content="Fresh Salads"),
                SemanticNode(id="cta1", section="cta", role="button", content="ORDER NOW")
            ]
        )
        brand = BrandKit(name="Healthy")
        generator = VariantGenerator()
        variants = generator.generate_variants(scene, "Instagram", brand)
        
        self.assertEqual(len(variants), 5)
        self.assertIn("Minimal", variants)
        self.assertIn("Modern", variants)
        self.assertIn("Premium", variants)
        self.assertIn("Bold", variants)
        self.assertIn("Luxury", variants)
        
        scorer = LayoutScorer()
        score = scorer.score(variants["Minimal"])
        self.assertTrue(0.0 <= score <= 100.0)

if __name__ == "__main__":
    unittest.main()
