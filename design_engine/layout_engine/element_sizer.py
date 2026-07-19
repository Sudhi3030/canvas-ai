from design_engine.scene_graph.node import Node, TextNode, ImageNode, ComponentNode
from design_engine.config import layout_rules

class ElementSizer:
    @staticmethod
    def size_elements(layout) -> None:
        """
        Pass 4: Sets element width and height dimensions based on relative hierarchy ratios before solving absolute offsets.
        """
        canvas_w = float(layout.canvas.width)
        canvas_h = float(layout.canvas.height)
        
        def traverse(node: Node):
            id_lower = node.id.lower()
            if isinstance(node, ImageNode) and ("hero" in id_lower or "product" in id_lower):
                node.width = canvas_w * 0.75
                node.height = canvas_h * layout_rules.HERO_SCALE
                node.width_policy = "fixed"
                node.height_policy = "fixed"
            elif isinstance(node, TextNode) and ("heading" in id_lower or "headline" in id_lower):
                node.properties.font_size = max(layout_rules.MIN_TEXT_SIZE, min(layout_rules.MAX_TEXT_SIZE, canvas_h * 0.05))
            elif isinstance(node, ComponentNode) and ("cta" in id_lower or "button" in id_lower):
                node.width = 240.0
                node.height = 60.0
                node.width_policy = "fixed"
                node.height_policy = "fixed"
            elif isinstance(node, ImageNode) and "logo" in id_lower:
                node.width = 80.0
                node.height = 80.0
                node.width_policy = "fixed"
                node.height_policy = "fixed"
                
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
