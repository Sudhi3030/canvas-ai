from design_engine.scene_graph.node import ComponentNode, ShadowEffect

class CTAEmphasis:
    @staticmethod
    def emphasize_cta(layout) -> None:
        """
        Pass 8: Sets CTA dimensions and shadow visual targets.
        """
        def traverse(node):
            if isinstance(node, ComponentNode) and ("cta" in node.id.lower() or "button" in node.id.lower()):
                node.width = 240.0
                node.height = 60.0
                node.effects = [
                    ShadowEffect(
                        type="drop_shadow",
                        color="#000000",
                        offset_x=0.0,
                        offset_y=6.0,
                        blur=12.0
                    )
                ]
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
