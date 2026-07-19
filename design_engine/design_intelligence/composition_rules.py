from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import ImageNode, TextNode

class CompositionRules:
    @staticmethod
    def select_layout_mode(layout: Layout) -> str:
        """
        Determines the optimal layout direction mode based on content availability.
        """
        has_image = False
        
        def check_node(node):
            nonlocal has_image
            if isinstance(node, ImageNode):
                has_image = True
            if hasattr(node, "children"):
                for child in node.children:
                    check_node(child)
                    
        for root in layout.scene_tree:
            check_node(root)
            
        if has_image:
            return "horizontal"
        return "vertical"
