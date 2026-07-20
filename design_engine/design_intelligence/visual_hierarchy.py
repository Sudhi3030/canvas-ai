from design_engine.scene_graph.node import Node, TextNode, ImageNode, ComponentNode

class VisualHierarchy:
    @staticmethod
    def assign_hierarchy(layout) -> None:
        """
        Pass 1: Assigns importance weights to nodes based on roles.
        """
        def traverse(node: Node):
            importance = 50.0
            id_lower = node.id.lower()
            if isinstance(node, ImageNode) and ("hero" in id_lower or "product" in id_lower):
                importance = 100.0
            elif isinstance(node, TextNode) and ("heading" in id_lower or "headline" in id_lower):
                importance = 90.0
            elif isinstance(node, ComponentNode) and ("cta" in id_lower or "button" in id_lower):
                importance = 80.0
            elif isinstance(node, TextNode) and ("body" in id_lower or "description" in id_lower):
                importance = 50.0
            elif isinstance(node, ImageNode) and "logo" in id_lower:
                importance = 30.0
                
            object.__setattr__(node, "importance", importance)
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
