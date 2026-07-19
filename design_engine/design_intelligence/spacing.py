from design_engine.scene_graph.document import Layout

class SpacingEvaluator:
    @staticmethod
    def evaluate_spacing(layout: Layout) -> float:
        """
        Scores margins and canvas boundary clearances.
        """
        margin_violations = 0
        w = layout.canvas.width
        h = layout.canvas.height
        
        for node in layout.scene_tree:
            if not node.visible:
                continue
            # Elements shouldn't lie inside a 10px canvas margin threshold
            if node.x < 10.0 or (node.x + node.width) > (w - 10.0) or \
               node.y < 10.0 or (node.y + node.height) > (h - 10.0):
                margin_violations += 1
                
        if margin_violations > 0:
            return max(40.0, 100.0 - margin_violations * 15.0)
        return 100.0
