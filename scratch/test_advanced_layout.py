import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import GroupNode, ShapeNode, ShapeProperties
from design_engine.layout_engine.layout import LayoutSolver

class TestAdvancedLayout(unittest.TestCase):
    def test_aspect_ratio_scaling(self):
        # ShapeNode with fixed width and height fit, and aspect ratio constraint
        node = ShapeNode(
            id="shape", name="Aspect Rect",
            width=200.0, height=100.0,
            width_policy="fixed", height_policy="fit",
            aspect_ratio=2.0, # width / height = 2.0 -> height = 100.0
            properties=ShapeProperties()
        )
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[node],
            metadata=Metadata()
        )
        solver = LayoutSolver()
        solver.solve(layout)
        
        self.assertEqual(node.width, 200.0)
        self.assertEqual(node.height, 100.0)

    def test_wrap_layout(self):
        # Wrap GroupNode of width 300 with spacing 10
        # Contains 3 children of width 100 -> Row 1 holds 2 items (100+10+100=210), Row 2 holds 1 item (100)
        c1 = ShapeNode(id="c1", name="Child 1", width=100.0, height=50.0, properties=ShapeProperties())
        c2 = ShapeNode(id="c2", name="Child 2", width=100.0, height=60.0, properties=ShapeProperties())
        c3 = ShapeNode(id="c3", name="Child 3", width=100.0, height=40.0, properties=ShapeProperties())
        
        wrap_group = GroupNode(
            id="wrap", name="Wrap Container",
            width=300.0, height=400.0,
            width_policy="fixed", height_policy="fit",
            layout_mode="wrap", spacing=10.0,
            padding_left=5.0, padding_top=5.0,
            cross_align="center" # Vertically align center within row heights
        )
        wrap_group.children = [c1, c2, c3]
        
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[wrap_group],
            metadata=Metadata()
        )
        solver = LayoutSolver()
        solver.solve(layout)
        
        # Row 1 height: max(50, 60) = 60
        # Row 2 height: max(40) = 40
        # Total wrap height = padding_top + 60 + spacing(10) + 40 + padding_bottom
        # padding_top(5) + 60 + 10 + 40 + padding_bottom(0) = 115.0
        self.assertEqual(wrap_group.height, 115.0)
        
        # Row 1 children positions:
        # c1.x = padding_left(5.0) = 5.0
        # c2.x = 5.0 + 100.0 + 10.0 = 115.0
        # Row 2 children positions:
        # c3.x = padding_left(5.0) = 5.0
        self.assertEqual(c1.x, 5.0)
        self.assertEqual(c2.x, 115.0)
        self.assertEqual(c3.x, 5.0)
        
        # Y-offsets (align center within row max height)
        # c1.y = padding_top(5.0) + (60 - 50)/2 = 10.0
        # c2.y = padding_top(5.0) + (60 - 60)/2 = 5.0
        # c3.y = padding_top(5.0) + row_1_h(60) + spacing(10) + (40 - 40)/2 = 75.0
        self.assertEqual(c1.y, 10.0)
        self.assertEqual(c2.y, 5.0)
        self.assertEqual(c3.y, 75.0)

if __name__ == "__main__":
    unittest.main()
