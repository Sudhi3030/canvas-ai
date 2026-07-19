from design_engine.config import layout_rules

class ConstraintSolver:
    @staticmethod
    def solve_constraints(layout) -> None:
        """
        Pass 5: Converts semantic region ratios to coordinate boundaries and enforces safe area constraints.
        """
        canvas_w = float(layout.canvas.width)
        canvas_h = float(layout.canvas.height)
        
        def traverse(node):
            node.x = max(layout_rules.SAFE_AREA, min(canvas_w - layout_rules.SAFE_AREA - node.width, node.x))
            node.y = max(layout_rules.SAFE_AREA, min(canvas_h - layout_rules.SAFE_AREA - node.height, node.y))
            
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)
                    
        for root in layout.scene_tree:
            traverse(root)
