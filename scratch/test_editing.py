import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.editing.intent_parser import IntentParser
from design_engine.editing.scene_modifier import SceneModifier
from design_engine.editing.history_manager import HistoryManager
from design_engine.editing.optimizer import EditingOptimizer
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import TextNode

class TestEditingEngine(unittest.TestCase):
    def test_intent_parsing(self):
        parser = IntentParser()
        intent = parser.parse("Make the title bigger")
        self.assertEqual(intent.action, "resize")
        self.assertEqual(intent.target, "title")
        self.assertEqual(intent.properties.get("font_size_scale"), 1.3)

    def test_scene_modification_and_history(self):
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[
                TextNode(
                    id="title_text", name="Main Title",
                    x=50, y=50, width=400, height=80,
                    properties={"content": "Main Title Text", "color": "#000000", "font_size": 20.0}
                )
            ],
            metadata=Metadata()
        )
        
        history = HistoryManager(max_depth=5)
        # Commit base state
        history.commit(layout)
        
        # Apply Resize Edit Command
        parser = IntentParser()
        intent = parser.parse("Make the title bigger")
        SceneModifier.apply_intent(layout, intent)
        
        node = layout.scene_tree[0]
        self.assertEqual(node.properties.font_size, 26.0) # 20.0 * 1.3 = 26.0
        
        # Undo resize command
        undone_layout = history.undo(layout)
        self.assertIsNotNone(undone_layout)
        undone_node = undone_layout.scene_tree[0]
        self.assertEqual(undone_node.properties.font_size, 20.0)

    def test_layout_recomputation_and_optimization(self):
        layout = Layout(
            canvas=Canvas(width=800, height=800),
            scene_tree=[
                TextNode(
                    id="header_text", name="Header Text",
                    x=5, y=5, width=400, height=80,
                    properties={"content": "Headline", "color": "#000000", "font_size": 16.0}
                ),
                TextNode(
                    id="body_text", name="Body Text",
                    x=50, y=150, width=400, height=80,
                    properties={"content": "Description text goes here.", "color": "#000000", "font_size": 15.0}
                )
            ],
            metadata=Metadata()
        )
        
        optimizer = EditingOptimizer()
        # Should solve constraints and trigger accessibility/hierarchy fixes
        fixes = optimizer.recompute_and_optimize(layout)
        self.assertTrue(len(fixes) > 0)
        
        # Header text node must be snapped away from boundary margin (x=15.0, y=15.0)
        node = layout.scene_tree[0]
        self.assertEqual(node.x, 15.0)
        self.assertEqual(node.y, 15.0)

if __name__ == "__main__":
    unittest.main()
