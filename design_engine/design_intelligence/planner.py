from design_engine.scene_graph.document import Layout
from design_engine.design_intelligence.layout_refiner import LayoutRefiner

class DesignIntelligencePlanner:
    def plan_and_refine(self, layout: Layout, style_name: str = "Modern") -> None:
        """
        Plans and refines layout document properties prior to rendering.
        """
        LayoutRefiner.refine(layout, style_name)
