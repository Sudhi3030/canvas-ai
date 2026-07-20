from design_engine.scene_graph.document import Layout
from design_engine.design_intelligence.visual_hierarchy import VisualHierarchy
from design_engine.design_intelligence.whitespace import WhitespaceOptimizer
from design_engine.design_intelligence.typography import TypographyOptimizer
from design_engine.design_intelligence.image_focus import ImageFocus
from design_engine.design_intelligence.composition import CompositionOptimizer
from design_engine.design_intelligence.balance import BalanceAnalyzer
from design_engine.design_intelligence.color_harmony import ColorHarmony
from design_engine.design_intelligence.emphasis import CTAEmphasis
from design_engine.design_intelligence.metrics import DesignMetrics
from design_engine.design_intelligence.scorer import DesignScorer
from design_engine.design_intelligence.debug import DesignDebug

class DesignIntelligenceEngine:
    @staticmethod
    def process(layout: Layout) -> None:
        """
        Runs the sequential Design Intelligence passes.
        """
        VisualHierarchy.assign_hierarchy(layout)
        WhitespaceOptimizer.optimize_whitespace(layout)
        TypographyOptimizer.optimize_typography(layout)
        ImageFocus.focus_images(layout)
        CompositionOptimizer.optimize_composition(layout)
        BalanceAnalyzer.analyze_balance(layout)
        ColorHarmony.apply_color_harmony(layout)
        CTAEmphasis.emphasize_cta(layout)
        
        # Evaluate design score
        scorer = DesignScorer()
        score_breakdown = scorer.evaluate(layout)
        
        # Compile detailed metrics
        DesignMetrics.compile_metrics(layout, score_breakdown.overall_score)
        
        # Render visual debug overlays
        DesignDebug.generate_debug_overlays(layout)
