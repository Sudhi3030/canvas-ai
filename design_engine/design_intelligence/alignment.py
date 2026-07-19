from design_engine.scene_graph.document import Layout

class AlignmentEvaluator:
    @staticmethod
    def evaluate_alignment(layout: Layout) -> float:
        """
        Scores element boundary alignments, penalizing overlapping child containers.
        """
        overlaps = 0
        nodes = [n for n in layout.scene_tree if n.visible]
        
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i+1:]:
                # Check overlap bounds
                overlap_x = not (n1.x + n1.width <= n2.x or n2.x + n2.width <= n1.x)
                overlap_y = not (n1.y + n1.height <= n2.y or n2.y + n2.height <= n1.y)
                if overlap_x and overlap_y:
                    overlaps += 1
        
        if overlaps > 0:
            return max(30.0, 100.0 - overlaps * 25.0)
        return 100.0
