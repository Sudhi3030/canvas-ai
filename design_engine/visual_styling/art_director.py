from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, TextNode, GroupNode
from design_engine.visual_styling.color_harmony import ColorHarmonyEngine
from design_engine.visual_styling.typography_pairing import TypographyPairingEngine
from design_engine.visual_styling.background_generator import BackgroundGenerator
from design_engine.visual_styling.card_generator import CardGenerator
from design_engine.visual_styling.decoration_generator import DecorationGenerator
from design_engine.visual_styling.depth_generator import DepthGenerator

class ArtDirector:
    @staticmethod
    def beautify(layout: Layout, style_name: str = "Modern") -> None:
        """
        Applies a cohesive visual styling direction to make a layout beautiful.
        """
        # 1. Resolve role palettes colors
        colors = ColorHarmonyEngine.get_colors(style_name)
        
        # 2. Resolve typography font pairing
        fonts = TypographyPairingEngine.get_pairing(style_name)
        
        # 3. Apply background treatment
        BackgroundGenerator.generate_background(layout, style_name, colors.neutral, colors.accent)
        
        # 4. Format headings & body typography properties
        def traverse_text(node: Node):
            if isinstance(node, TextNode):
                if "header" in node.id.lower() or "headline" in node.id.lower():
                    node.properties.font_family = fonts.heading
                    node.properties.letter_spacing = fonts.letter_spacing
                    node.properties.color = colors.primary
                else:
                    node.properties.font_family = fonts.body
                    node.properties.color = colors.secondary
                    
            if isinstance(node, GroupNode):
                for child in node.children:
                    traverse_text(child)

        for root in layout.scene_tree:
            traverse_text(root)
            
        # 5. Format cards opacity and border radiuses
        CardGenerator.style_cards(layout, style_name, colors.surface, colors.border)
        
        # 6. Inject abstract shapes
        DecorationGenerator.inject_decorations(layout, style_name, colors.accent)
        
        # 7. Apply shadows depth elevation
        DepthGenerator.apply_shadows(layout, style_name, colors.shadow)
