from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, TextNode, ShapeNode, GroupNode
from design_engine.design_intelligence.design_tokens import DesignTokens

class StyleSelector:
    @staticmethod
    def apply_style(layout: Layout, style_name: str) -> None:
        """
        Applies brand kit or custom color theme styling to canvas and visual elements.
        """
        tokens = DesignTokens()
        palette = next((p for p in tokens.palettes if p.name.lower() == style_name.lower()), tokens.palettes[0])
        
        layout.canvas.background_color = palette.background
        
        def traverse(node: Node):
            if isinstance(node, TextNode):
                if "header" in node.id.lower() or "headline" in node.id.lower():
                    node.properties.color = palette.primary
                else:
                    node.properties.color = palette.secondary
            elif isinstance(node, ShapeNode):
                if "bg" in node.id.lower() or "panel" in node.id.lower():
                    node.properties.fill_color = palette.background
                else:
                    node.properties.fill_color = palette.accent
                    
            if isinstance(node, GroupNode):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
