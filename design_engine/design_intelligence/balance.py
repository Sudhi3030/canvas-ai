from design_engine.scene_graph.document import Layout

class BalanceEngine:
    @staticmethod
    def calculate_balance(layout: Layout) -> float:
        """
        Calculates left-right visual symmetry scores.
        """
        from design_engine.design_intelligence.composition import CompositionEvaluator
        return CompositionEvaluator.evaluate_composition(layout)

class BalanceAnalyzer:
    @staticmethod
    def analyze_balance(layout: Layout) -> float:
        """
        Pass 6: Computes left vs right visual weight balance and symmetry.
        """
        from design_engine.design_intelligence.composition import CompositionEvaluator
        score = CompositionEvaluator.evaluate_composition(layout)
        object.__setattr__(layout, "balance_score", score)
        return score
