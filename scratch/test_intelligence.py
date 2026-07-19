import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.design_intelligence.scorer import DesignScorer
from design_engine.design_intelligence.optimizer import DesignOptimizer
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import TextNode

class TestDesignIntelligence(unittest.TestCase):
    def test_design_scoring(self):
        scorer = DesignScorer()
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[
                TextNode(
                    id="t1", name="Heading",
                    x=50, y=50, width=400, height=80,
                    properties={"content": "Low contrast heading", "color": "#0F172A", "font_size": 14.0}
                )
            ],
            metadata=Metadata()
        )
        breakdown = scorer.evaluate(layout)
        self.assertIsNotNone(breakdown)
        self.assertTrue(0.0 <= breakdown.overall_score <= 100.0)

    def test_auto_repair_loop(self):
        optimizer = DesignOptimizer(quality_threshold=80.0, max_iterations=2)
        layout = Layout(
            canvas=Canvas(width=800, height=800, background_color="#000000"),
            scene_tree=[
                TextNode(
                    id="t1", name="Low contrast label",
                    x=5, y=5, width=400, height=80,
                    # color is very close to canvas background color, size is small
                    properties={"content": "Label text", "color": "#111111", "font_size": 16.0}
                )
            ],
            metadata=Metadata()
        )
        
        # Optimize will execute repair passes to fix contrast and padding clearances
        fixes = optimizer.optimize(layout)
        self.assertTrue(len(fixes) > 0)
        
        # The node should be pushed away from the canvas edges (x=15.0, y=15.0)
        node = layout.scene_tree[0]
        self.assertEqual(node.x, 15.0)
        self.assertEqual(node.y, 15.0)
        # The contrast was auto-fixed to white #FFFFFF
        self.assertEqual(node.properties.color.upper(), "#FFFFFF")

if __name__ == "__main__":
    unittest.main()
