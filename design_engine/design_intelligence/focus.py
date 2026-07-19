from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, ComponentNode, GroupNode, ImageNode, TextNode

class FocusEngine:
    @staticmethod
    def highlight_focal_point(layout: Layout) -> None:
        """
        Enhances the sizing parameters of hero images, text headlines, and CTA button elements to draw focal attention.
        """
        canvas_w = float(layout.canvas.width)
        canvas_h = float(layout.canvas.height)
        
        def traverse(node: Node):
            # 1. Scale Hero Images to occupy 35% - 50% of canvas height area
            if isinstance(node, ImageNode) and ("hero" in node.id.lower() or "product" in node.id.lower()):
                node.width = max(node.width, canvas_w * 0.75)
                node.height = max(node.height, canvas_h * 0.45)
                node.width_policy = "fixed"
                node.height_policy = "fixed"
                
            # 2. Scale Headline Fonts
            elif isinstance(node, TextNode) and ("heading" in node.id.lower() or "headline" in node.id.lower()):
                node.properties.font_size = max(node.properties.font_size, 48.0 if canvas_w >= 800 else 36.0)
                
            # 3. Boost CTA buttons
            elif isinstance(node, ComponentNode) and ("cta" in node.id.lower() or "button" in node.id.lower()):
                node.width = max(node.width, 240.0)
                node.height = max(node.height, 60.0)
                node.width_policy = "fixed"
                node.height_policy = "fixed"
                
            if isinstance(node, GroupNode):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
