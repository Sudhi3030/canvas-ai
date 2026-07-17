import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.typography.layout import TypographyEngine
from design_engine.assets.manager import AssetManager
from design_engine.renderer.canvas_renderer import CanvasRenderer
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import TextNode

class TestTypographyEngine(unittest.TestCase):
    def test_text_wrapping_measurements(self):
        manager = AssetManager()
        layout_data = TypographyEngine.layout_text(
            content="This is a test block of text that wraps.",
            font_family="Arial",
            font_size=24.0,
            width=300.0,
            height=100.0,
            line_height=1.2,
            letter_spacing=1.0,
            align="center",
            vertical_align="middle",
            asset_manager=manager
        )
        self.assertIsNotNone(layout_data)
        self.assertTrue(len(layout_data["lines"]) > 0)
        self.assertEqual(layout_data["font_size"], 24.0)

    def test_auto_fitting(self):
        manager = AssetManager()
        # High font size inside tight container should force shrinking
        layout_data = TypographyEngine.layout_text(
            content="This is a long sentence that will definitely overflow the height threshold of this small container.",
            font_family="Arial",
            font_size=40.0,
            width=200.0,
            height=50.0,
            line_height=1.2,
            letter_spacing=0.0,
            align="left",
            vertical_align="top",
            asset_manager=manager
        )
        self.assertIsNotNone(layout_data)
        self.assertTrue(layout_data["font_size"] < 40.0)

    def test_renderer_integration(self):
        manager = AssetManager()
        renderer = CanvasRenderer(asset_manager=manager)
        layout = Layout(
            canvas=Canvas(width=600, height=600, background_color="#FFFFFF"),
            scene_tree=[
                TextNode(
                    id="header", name="Typography Title",
                    x=100, y=100, width=400, height=150,
                    properties={
                        "content": "TYPOGRAPHY ENGINE",
                        "font_family": "Georgia",
                        "font_size": 36.0,
                        "color": "#1E293B",
                        "align": "center",
                        "vertical_align": "middle",
                        "stroke_color": "#FFC107",
                        "stroke_width": 2
                    }
                ),
                TextNode(
                    id="body", name="Body Copy",
                    x=100, y=300, width=400, height=200,
                    properties={
                        "content": "This body copy is auto-fitting inside a fixed container. It should wrap and scale down correctly if the height constraints are violated.",
                        "font_family": "Arial",
                        "font_size": 24.0,
                        "color": "#0F172A",
                        "align": "left",
                        "vertical_align": "top"
                    }
                )
            ],
            metadata=Metadata()
        )
        out_path = renderer.render(layout, filename="test_typography_engine_e2e.png")
        self.assertTrue(os.path.exists(out_path))

if __name__ == "__main__":
    unittest.main()
