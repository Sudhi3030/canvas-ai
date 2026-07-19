import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.design_intelligence.layout_refiner import LayoutRefiner
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import TextNode, ComponentNode

class TestDesignIntelligencePipeline(unittest.TestCase):
    def test_layout_refinement(self):
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[
                TextNode(
                    id="header_text", name="Main Title",
                    x=50, y=50, width=400, height=80,
                    properties={"content": "Headline", "color": "#000000", "font_size": 24.0}
                ),
                ComponentNode(
                    id="cta_button", name="CTA Button",
                    x=50, y=200, width=100, height=40
                )
            ],
            metadata=Metadata()
        )
        
        # Run Refinement
        LayoutRefiner.refine(layout, "Premium")
        
        # 1. Colors updated based on palette background color
        self.assertEqual(layout.canvas.background_color, "#F8FAFC")
        
        # 2. CTA button size boosted as focal point
        cta = [n for n in layout.scene_tree if "cta" in n.id.lower()][0]
        self.assertEqual(cta.width, 180.0)
        self.assertEqual(cta.height, 50.0)
        
        # 3. Floating decoration abstract shape injected at the beginning
        self.assertTrue(len(layout.scene_tree) > 2)
        self.assertEqual(layout.scene_tree[0].id, "accent_blob_bg")

if __name__ == "__main__":
    unittest.main()
