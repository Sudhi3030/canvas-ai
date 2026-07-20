from design_engine.scene_graph.node import ImageNode

class ImageFocus:
    @staticmethod
    def focus_images(layout) -> None:
        """
        Pass 4: Scales and centers hero images to cover 35%-50% height of canvas.
        """
        canvas_w = float(layout.canvas.width)
        canvas_h = float(layout.canvas.height)
        
        def traverse(node):
            if isinstance(node, ImageNode) and ("hero" in node.id.lower() or "product" in node.id.lower()):
                node.width = canvas_w * 0.8
                node.height = canvas_h * 0.45
                node.width_policy = "fixed"
                node.height_policy = "fixed"
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
