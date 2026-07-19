from design_engine.scene_graph.document import Layout
from design_engine.design_intelligence.style_selector import StyleSelector
from design_engine.design_intelligence.composer import Composer
from design_engine.design_intelligence.focus import FocusEngine
from design_engine.design_intelligence.decorations import DecorationEngine
from design_engine.design_intelligence.metrics import DesignMetrics

class LayoutRefiner:
    @staticmethod
    def refine(layout: Layout, style_name: str = "Modern") -> None:
        """
        Coordinates the application of styling, composition rules, focus points,
        and abstract decorations to refine raw layouts.
        """
        # 1. Apply style colors matching theme
        StyleSelector.apply_style(layout, style_name)
        
        # 2. Select composition rules layout direction
        Composer.apply_composition(layout)
        
        # 3. Boost primary element focus sizing
        FocusEngine.highlight_focal_point(layout)
        
        # 4. Inject abstract graphical decorations
        DecorationEngine.inject_decorations(layout)
        
        # 5. Record refined metrics status
        DesignMetrics.compile_metrics(layout, 86.0)
