from design_engine.scene_graph.node import GroupNode

class WhitespaceOptimizer:
    @staticmethod
    def optimize_whitespace(layout) -> None:
        """
        Pass 2: Adjusts spacing and padding sizes.
        """
        canvas_h = float(layout.canvas.height)
        
        def traverse(node):
            if isinstance(node, GroupNode):
                node.spacing = max(15.0, canvas_h * 0.02)
                node.padding_left = max(30.0, canvas_h * 0.04)
                node.padding_top = max(40.0, canvas_h * 0.05)
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
