from design_engine.config import layout_rules
from design_engine.scene_graph.node import GroupNode

class SpacingOptimizer:
    @staticmethod
    def optimize_spacing(layout) -> None:
        """
        Pass 7: Enforces vertical spacing rhythm and optical gap padding.
        """
        def traverse(node):
            if isinstance(node, GroupNode):
                node.spacing = max(layout_rules.MIN_GAP, min(layout_rules.MAX_GAP, node.spacing))
                node.padding_left = max(layout_rules.MIN_MARGIN, node.padding_left)
                node.padding_top = max(layout_rules.MIN_MARGIN, node.padding_top)
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
