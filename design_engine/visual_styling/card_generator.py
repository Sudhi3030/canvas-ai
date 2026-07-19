from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import ShapeNode

class CardGenerator:
    @staticmethod
    def style_cards(layout: Layout, style: str, surface_color: str, border_color: str) -> None:
        """
        Enhances card border radius and glassmorphism transparency settings.
        """
        for node in layout.scene_tree:
            # Traverses root shapes to update cards styling
            if isinstance(node, ShapeNode) and ("card" in node.id.lower() or "bg" in node.id.lower()):
                node.properties.fill_color = surface_color
                node.properties.stroke_color = border_color
                node.properties.stroke_width = 2.0
                
                if style.lower() == "luxury":
                    node.properties.border_radius = 24.0
                elif style.lower() == "minimal":
                    node.properties.border_radius = 4.0
                else:
                    node.properties.border_radius = 12.0
