from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import GroupNode
from design_engine.design_intelligence.composition_rules import CompositionRules

class Composer:
    @staticmethod
    def apply_composition(layout: Layout) -> None:
        """
        Adjusts group layout configurations based on chosen composition flow settings.
        """
        mode = CompositionRules.select_layout_mode(layout)
        
        def traverse(node):
            if isinstance(node, GroupNode):
                node.layout_mode = mode
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
