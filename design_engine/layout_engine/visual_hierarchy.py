from design_engine.scene_graph.node import Node, TextNode, ImageNode, ComponentNode

class VisualHierarchyEngine:
    @staticmethod
    def assign_hierarchy_importance(layout) -> None:
        """
        Pass 1: Traverses the scene graph to analyze node types and assign relative priorities.
        """
        def traverse(node: Node):
            importance = 50.0
            visual_weight = 0.50
            emphasis = "secondary"
            
            id_lower = node.id.lower()
            if isinstance(node, ImageNode) and ("hero" in id_lower or "product" in id_lower):
                importance = 100.0
                visual_weight = 0.95
                emphasis = "primary"
            elif isinstance(node, TextNode) and ("heading" in id_lower or "headline" in id_lower):
                importance = 95.0
                visual_weight = 0.90
                emphasis = "primary"
            elif isinstance(node, ComponentNode) and ("cta" in id_lower or "button" in id_lower):
                importance = 70.0
                visual_weight = 0.70
                emphasis = "primary"
            elif isinstance(node, TextNode) and ("body" in id_lower or "description" in id_lower):
                importance = 40.0
                visual_weight = 0.30
                emphasis = "muted"
                
            # Assign properties
            object.__setattr__(node, "importance", importance)
            
            prio = {
                "importance": importance,
                "visual_weight": visual_weight,
                "emphasis": emphasis
            }
            object.__setattr__(node, "visual_priority", prio)
                
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
