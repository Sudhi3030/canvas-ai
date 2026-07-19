from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import TextNode

class HierarchyEvaluator:
    @staticmethod
    def evaluate_hierarchy(layout: Layout) -> float:
        """
        Scores typography size scales, rewarding headings that are at least 1.5x larger than body text.
        """
        headings = [n for n in layout.scene_tree if isinstance(n, TextNode) and ("header" in n.id.lower() or "headline" in n.id.lower())]
        bodies = [n for n in layout.scene_tree if isinstance(n, TextNode) and ("body" in n.id.lower() or "description" in n.id.lower())]
        
        if not headings or not bodies:
            return 80.0 # Default base if elements are not present to compare
            
        max_heading_size = max(h.properties.font_size for h in headings)
        max_body_size = max(b.properties.font_size for b in bodies)
        
        if max_heading_size >= max_body_size * 1.5:
            return 100.0
        elif max_heading_size >= max_body_size * 1.2:
            return 80.0
        else:
            return 50.0
