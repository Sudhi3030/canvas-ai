from design_engine.scene_graph.node import TextNode

class TypographyOptimizer:
    @staticmethod
    def optimize_typography(layout) -> None:
        """
        Pass 3: Dynamically adjusts font sizes based on canvas width.
        """
        canvas_w = float(layout.canvas.width)
        
        def traverse(node):
            if isinstance(node, TextNode):
                id_lower = node.id.lower()
                if "heading" in id_lower or "headline" in id_lower:
                    node.properties.font_size = 64.0 if canvas_w >= 1000 else 48.0
                elif "body" in id_lower or "description" in id_lower:
                    node.properties.font_size = 22.0 if canvas_w >= 1000 else 18.0
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
