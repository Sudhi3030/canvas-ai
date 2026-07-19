from design_engine.scene_graph.document import Layout
from design_engine.design_intelligence.models import ScoreBreakdown, MetricScore
from design_engine.design_intelligence.hierarchy import HierarchyEvaluator
from design_engine.design_intelligence.composition import CompositionEvaluator
from design_engine.design_intelligence.alignment import AlignmentEvaluator
from design_engine.design_intelligence.spacing import SpacingEvaluator
from design_engine.scene_graph.node import ImageNode, ComponentNode, TextNode

class DesignScorer:
    def evaluate(self, layout: Layout) -> ScoreBreakdown:
        """
        Runs multiple design audits to build a detailed aesthetic score report.
        """
        h_score = HierarchyEvaluator.evaluate_hierarchy(layout)
        b_score = CompositionEvaluator.evaluate_composition(layout)
        a_score = AlignmentEvaluator.evaluate_alignment(layout)
        s_score = SpacingEvaluator.evaluate_spacing(layout)
        
        # Contrast / Readability
        c_score = 100.0
        from design_engine.design_rules.accessibility import relative_luminance
        
        bg_color = layout.canvas.background_color
        bg_lum = relative_luminance(bg_color)
        
        for node in layout.scene_tree:
            if not node.visible or not isinstance(node, TextNode):
                continue
            text_lum = relative_luminance(node.properties.color)
            l1, l2 = max(bg_lum, text_lum), min(bg_lum, text_lum)
            ratio = (l1 + 0.05) / (l2 + 0.05)
            
            if ratio < 4.5:
                c_score = max(40.0, c_score - 20.0)

        # 1. Overlap (10%)
        overlap_score = a_score
        
        # 2. Alignment (15%)
        alignment_score = a_score
        
        # 3. White Space (15%)
        whitespace_score = s_score
        
        # 4. Visual Hierarchy (20%)
        hierarchy_score = h_score
        
        # 5. Readability (15%)
        readability_score = c_score
        
        # 6. Hero Prominence (15%)
        canvas_w = float(layout.canvas.width)
        canvas_h = float(layout.canvas.height)
        canvas_area = canvas_w * canvas_h
        
        hero_score = 70.0
        def find_hero(node):
            nonlocal hero_score
            if isinstance(node, ImageNode) and ("hero" in node.id.lower() or "product" in node.id.lower()):
                node_area = float(node.width) * float(node.height or 0.0)
                if node_area >= canvas_area * 0.15:
                    hero_score = 100.0
            if hasattr(node, "children"):
                for child in node.children:
                    find_hero(child)

        for root in layout.scene_tree:
            find_hero(root)
            
        # 7. CTA Visibility (10%)
        cta_score = 70.0
        def find_cta(node):
            nonlocal cta_score
            if isinstance(node, ComponentNode) and ("cta" in node.id.lower() or "button" in node.id.lower()):
                if node.width >= 200.0 and node.height >= 50.0:
                    cta_score = 100.0
            if hasattr(node, "children"):
                for child in node.children:
                    find_cta(child)

        for root in layout.scene_tree:
            find_cta(root)

        # Calculate weighted sum
        overall = (
            (overlap_score * 0.10) +
            (alignment_score * 0.15) +
            (whitespace_score * 0.15) +
            (hierarchy_score * 0.20) +
            (readability_score * 0.15) +
            (hero_score * 0.15) +
            (cta_score * 0.10)
        )
        
        return ScoreBreakdown(
            hierarchy=MetricScore(score=hierarchy_score, details="Visual typographic hierarchy rules"),
            alignment=MetricScore(score=alignment_score, details="Element overlap checks"),
            spacing=MetricScore(score=whitespace_score, details="Border clearances spacing scale"),
            balance=MetricScore(score=b_score, details="Left-to-right area composition balance"),
            contrast=MetricScore(score=readability_score, details="Text WCAG contrast compliance levels"),
            accessibility=MetricScore(score=c_score, details="Platform safe targets constraints"),
            overall_score=overall
        )
