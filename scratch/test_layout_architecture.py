import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.layout_engine.layout import LayoutSolver
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import ImageNode, TextNode, ComponentNode

class TestLayoutArchitecture(unittest.TestCase):
    def test_decoupled_layout_solver_pipeline(self):
        hero = ImageNode(
            id="hero", name="Hero Image", x=0, y=0, width=300, height=200,
            properties={"url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&q=80"}
        )
        heading = TextNode(
            id="heading", name="Heading",
            properties={"content": "Salads", "color": "#000000", "font_size": 24.0}
        )
        body = TextNode(
            id="body", name="Description",
            properties={"content": "copy text", "color": "#000000", "font_size": 16.0}
        )
        
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[hero, heading, body],
            metadata=Metadata(template="Split Layout")
        )
        
        solver = LayoutSolver()
        solver.solve(layout)
        
        # 1. Verify Visual Hierarchy Engine relative priority assignments
        hero_prio = getattr(hero, "visual_priority", {})
        head_prio = getattr(heading, "visual_priority", {})
        body_prio = getattr(body, "visual_priority", {})
        
        self.assertGreater(hero_prio.get("importance", 0.0), body_prio.get("importance", 0.0))
        self.assertGreater(head_prio.get("importance", 0.0), body_prio.get("importance", 0.0))
        
        # 2. Verify safe area padding constraint is solved
        self.assertTrue(hero.x >= 0.0)
        self.assertTrue(hero.y >= 0.0)

if __name__ == "__main__":
    unittest.main()
