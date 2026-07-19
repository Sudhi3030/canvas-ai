from design_engine.scene_graph.document import Layout

class BalanceEngine:
    @staticmethod
    def calculate_balance(layout: Layout) -> float:
        """
        Calculates left-right visual symmetry scores.
        """
        from design_engine.design_intelligence.composition import CompositionEvaluator
        return CompositionEvaluator.evaluate_composition(layout)
