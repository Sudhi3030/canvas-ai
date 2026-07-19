from design_engine.scene_graph.document import Layout
from design_engine.design_intelligence.scorer import DesignScorer

class LayoutScorer:
    def score(self, layout: Layout) -> float:
        """
        Heuristically scores a layout from 0.0 to 100.0 based on visual quality.
        """
        scorer = DesignScorer()
        breakdown = scorer.evaluate(layout)
        return breakdown.overall_score
