from typing import List, Any
from design_engine.scene_graph.document import Layout
from design_engine.design_intelligence.optimizer import DesignOptimizer as AIDesignOptimizer

class DesignOptimizer:
    def __init__(self, rules_engine: Any = None, quality_threshold: float = 75.0, max_iterations: int = 3):
        self.ai_optimizer = AIDesignOptimizer(quality_threshold=quality_threshold, max_iterations=max_iterations)

    def optimize(self, layout: Layout) -> List[str]:
        """
        Applies rules-based layout adjustments to optimize whitespace, contrast, and alignment.
        """
        return self.ai_optimizer.optimize(layout)
