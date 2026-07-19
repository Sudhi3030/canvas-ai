from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, ShadowEffect, GroupNode

class DepthGenerator:
    @staticmethod
    def apply_shadows(layout: Layout, style: str, shadow_color: str) -> None:
        """
        Adds professional drop shadows to visual nodes to construct visual depth levels.
        """
        if style.lower() == "minimal":
            return
            
        shadow = ShadowEffect(
            type="drop_shadow",
            color=shadow_color,
            offset_x=0.0,
            offset_y=8.0,
            blur=16.0
        )
        
        def traverse(node: Node):
            if hasattr(node, "effects"):
                node.effects = [shadow]
            if isinstance(node, GroupNode):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
