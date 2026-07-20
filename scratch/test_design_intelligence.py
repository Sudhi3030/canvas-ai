import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.design_intelligence.engine import DesignIntelligenceEngine
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import ImageNode, TextNode, ComponentNode

class TestDesignIntelligence(unittest.TestCase):
    def test_design_intelligence_pipeline(self):
        hero = ImageNode(
            id="hero", name="Hero Image", x=0, y=0, width=300, height=200,
            properties={"url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&q=80"}
        )
        heading = TextNode(
            id="heading", name="Heading",
            properties={"content": "Salads", "color": "#000000", "font_size": 24.0}
        )
        
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[hero, heading],
            metadata=Metadata(template="Split Layout")
        )
        
        DesignIntelligenceEngine.process(layout)
        
        # 1. Verify Visual Hierarchy assigned priority
        self.assertEqual(getattr(hero, "importance", None), 100.0)
        
        # 2. Verify Hero Image occupies 35-50% height (800 * 0.45 = 360)
        self.assertTrue(300.0 <= hero.height <= 400.0)
        
        # 3. Verify metrics compiled
        metrics = getattr(layout, "metrics", {})
        self.assertIn("balance", metrics)

if __name__ == "__main__":
    unittest.main()
