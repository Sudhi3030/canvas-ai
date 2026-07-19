from design_engine.scene_graph.document import Layout

class CompositionEvaluator:
    @staticmethod
    def evaluate_composition(layout: Layout) -> float:
        """
        Scores structural composition by checking the weight symmetry (left-right area ratio balance).
        """
        mid_x = layout.canvas.width / 2.0
        
        left_weight = 0.0
        right_weight = 0.0
        
        for node in layout.scene_tree:
            if not node.visible:
                continue
            center_x = node.x + node.width / 2.0
            area = node.width * node.height
            if center_x < mid_x:
                left_weight += area
            else:
                right_weight += area
                
        total = left_weight + right_weight
        if total <= 0:
            return 100.0
            
        ratio = abs(left_weight - right_weight) / total
        if ratio <= 0.4:
            return 100.0
        elif ratio <= 0.7:
            return 75.0
        else:
            return 50.0
