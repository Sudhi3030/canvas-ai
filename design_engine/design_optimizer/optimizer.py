from typing import List
from design_engine.scene_graph.document import Layout
from design_engine.design_rules.accessibility import DesignRulesEngine

class DesignOptimizer:
    def __init__(self, rules_engine: DesignRulesEngine = None):
        self.rules_engine = rules_engine or DesignRulesEngine()

    def optimize(self, layout: Layout) -> List[str]:
        """
        Applies rules-based layout adjustments to optimize whitespace, contrast, and alignment.
        """
        return self.rules_engine.analyze_and_fix(layout)
