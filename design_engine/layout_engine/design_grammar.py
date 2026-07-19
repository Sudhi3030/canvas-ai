from design_engine.scene_graph.node import Node, GroupNode, ImageNode, TextNode

class DesignGrammarEngine:
    @staticmethod
    def apply_grammar_rules(layout, strategy: str) -> None:
        """
        Enforces professional design grammar alignments on components.
        """
        def traverse(node: Node):
            # Rule 1: Set text alignment based on composition symmetry
            if isinstance(node, TextNode) and ("heading" in node.id.lower() or "headline" in node.id.lower()):
                if "EDITORIAL" in strategy or "SPLIT" in strategy or "MINIMAL" in strategy:
                    node.properties.align = "left"
                else:
                    node.properties.align = "center"
            
            # Rule 2: Ensure logo node is always placed top in the parent flow stack
            if isinstance(node, GroupNode) and node.layout_mode == "vertical":
                logo_idx = -1
                for idx, child in enumerate(node.children):
                    if isinstance(child, ImageNode) and "logo" in child.id.lower():
                        logo_idx = idx
                        break
                if logo_idx > 0:
                    logo_node = node.children.pop(logo_idx)
                    node.children.insert(0, logo_node)
                    
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
