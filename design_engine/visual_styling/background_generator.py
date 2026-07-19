from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import ShapeNode, GradientProperties

class BackgroundGenerator:
    @staticmethod
    def generate_background(layout: Layout, style: str, bg_color: str, accent_color: str) -> None:
        """
        Alters canvas background and injects a card layout panel pattern.
        """
        layout.canvas.background_color = bg_color
        
        # Add linear gradients for modern, luxury, or elegant styles
        if style.lower() in ("luxury", "modern", "elegant"):
            for node in layout.scene_tree:
                # Find main container panel shapes
                if isinstance(node, ShapeNode) and ("bg" in node.id.lower() or "panel" in node.id.lower()):
                    node.properties.fill_gradient = GradientProperties(
                        colors=[bg_color, accent_color],
                        angle=45.0
                    )
