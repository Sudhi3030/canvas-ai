from design_engine.scene_graph.node import TextNode

class AlignmentEngine:
    @staticmethod
    def align_elements(layout, strategy: str) -> None:
        """
        Pass 6: Aligns text elements visually based on composition style before spacing optimizations.
        """
        def traverse(node):
            if isinstance(node, TextNode):
                if "EDITORIAL" in strategy or "SPLIT" in strategy or "MINIMAL" in strategy:
                    node.properties.align = "left"
                else:
                    node.properties.align = "center"
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
