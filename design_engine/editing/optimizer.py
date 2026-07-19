from design_engine.scene_graph.document import Layout
from design_engine.layout_engine.layout import LayoutSolver
from design_engine.design_intelligence.optimizer import DesignOptimizer as AIDesignOptimizer

class EditingOptimizer:
    def __init__(self):
        self.solver = LayoutSolver()
        self.ai_optimizer = AIDesignOptimizer(quality_threshold=80.0, max_iterations=2)

    def recompute_and_optimize(self, layout: Layout) -> list[str]:
        """
        Recomputes layout spatial coordinates and runs Design Intelligence auto-repairs.
        """
        # 1. Solve layout constraints
        self.solver.solve(layout)
        
        # 2. Run aesthetic checks and auto-fixes
        return self.ai_optimizer.optimize(layout)
