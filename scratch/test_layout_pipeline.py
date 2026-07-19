import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.layout_engine.layout import LayoutSolver
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import ImageNode, TextNode

class TestLayoutPipeline(unittest.TestCase):
    def test_ten_passes_layout_pipeline(self):
        hero = ImageNode(
            id="hero", name="Hero Image", x=0, y=0, width=300, height=200,
            properties={"url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&q=80"}
        )
        heading = TextNode(
            id="heading", name="Headline Text",
            properties={"content": "Big Headline", "font_size": 24.0}
        )
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[hero, heading],
            metadata=Metadata(template="Split Layout")
        )
        
        solver = LayoutSolver()
        solver.solve(layout)
        
        # 1. Assert Visual Hierarchy score is registered
        importance = getattr(hero, "importance", None)
        self.assertEqual(importance, 100.0)
        
        # 2. Hero inside canvas
        self.assertGreaterEqual(hero.x, 0)
        self.assertGreaterEqual(hero.y, 0)
        self.assertLessEqual(hero.x + hero.width, layout.canvas.width)
        self.assertLessEqual(hero.y + hero.height, layout.canvas.height)
        
        # 3. Metrics generated
        metrics = getattr(layout.metadata, "metrics", {})
        self.assertIn("whitespace_ratio", metrics)
        
        # 4. Verify debug overlays files exist
        self.assertTrue(os.path.exists("outputs/debug/regions.png"))
        self.assertTrue(os.path.exists("outputs/debug/hierarchy.png"))

if __name__ == "__main__":
    unittest.main()
