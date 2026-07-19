import logging
from design_engine.scene_graph.document import Layout
from design_engine.design_intelligence.scorer import DesignScorer
from design_engine.design_intelligence.repair import DesignRepairer

logger = logging.getLogger("DesignOptimizer")

class DesignOptimizer:
    def __init__(self, quality_threshold: float = 75.0, max_iterations: int = 3):
        self.scorer = DesignScorer()
        self.repairer = DesignRepairer()
        self.quality_threshold = quality_threshold
        self.max_iterations = max_iterations

    def optimize(self, layout: Layout) -> list[str]:
        """
        Iteratively scores, refines, and improves layout structure until quality goals are achieved.
        """
        fixes = []
        for iteration in range(self.max_iterations):
            breakdown = self.scorer.evaluate(layout)
            logger.info(f"Design Intelligence Scorer Iteration {iteration+1}: Score = {breakdown.overall_score:.1f}/100.0")
            
            if breakdown.overall_score >= self.quality_threshold:
                break
            
            # Apply repair modifications
            pass_fixes = self.repairer.repair_pass(layout, breakdown)
            fixes.extend(pass_fixes)
            
        return fixes
