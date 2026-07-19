from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import TextNode
from design_engine.design_intelligence.models import ScoreBreakdown

class DesignRepairer:
    def repair_pass(self, layout: Layout, breakdown: ScoreBreakdown) -> list[str]:
        """
        Executes targeted modifications to fix layout rules failures and returns repair logs.
        """
        fixes = []
        
        # 1. Repair Contrast issues
        if breakdown.contrast.score < 90.0:
            from design_engine.design_rules.accessibility import relative_luminance
            bg_color = layout.canvas.background_color
            bg_lum = relative_luminance(bg_color)
            for node in layout.scene_tree:
                if isinstance(node, TextNode):
                    text_lum = relative_luminance(node.properties.color)
                    l1, l2 = max(bg_lum, text_lum), min(bg_lum, text_lum)
                    ratio = (l1 + 0.05) / (l2 + 0.05)
                    if ratio < 4.5:
                        old_color = node.properties.color
                        node.properties.color = "#FFFFFF" if bg_lum < 0.5 else "#0F172A"
                        fixes.append(
                            f"Contrast ratio ({ratio:.1f}:1) for '{node.name}' was below WCAG threshold. "
                            f"Auto-fixed text color to '{node.properties.color}'."
                        )

        # 2. Repair Spacing / Margins issues
        if breakdown.spacing.score < 90.0:
            w = layout.canvas.width
            h = layout.canvas.height
            for node in layout.scene_tree:
                if not node.visible:
                    continue
                if node.x < 10.0 or (node.x + node.width) > (w - 10.0) or \
                   node.y < 10.0 or (node.y + node.height) > (h - 10.0):
                    node.x = max(15.0, min(node.x, w - node.width - 15.0))
                    node.y = max(15.0, min(node.y, h - node.height - 15.0))
                    fixes.append(f"Auto-adjusted node '{node.name}' margins to fit canvas safety area.")

        # 3. Repair Typography Hierarchy scales
        if breakdown.hierarchy.score < 90.0:
            headings = [n for n in layout.scene_tree if isinstance(n, TextNode) and ("header" in n.id.lower() or "headline" in n.id.lower())]
            bodies = [n for n in layout.scene_tree if isinstance(n, TextNode) and ("body" in n.id.lower() or "description" in n.id.lower())]
            if headings and bodies:
                max_body_size = max(b.properties.font_size for b in bodies)
                for h in headings:
                    if h.properties.font_size < max_body_size * 1.5:
                        old_size = h.properties.font_size
                        h.properties.font_size = max_body_size * 1.6
                        fixes.append(
                            f"Auto-scaled heading '{h.name}' font size from {old_size:.1f}pt to {h.properties.font_size:.1f}pt to improve visual hierarchy."
                        )
                        
        return fixes
