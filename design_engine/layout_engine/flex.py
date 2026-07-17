from typing import List, Any
from design_engine.layout_engine.alignment import AlignmentEngine

class FlexSolver:
    @staticmethod
    def solve_wrap(
        children: List[Any],
        avail_w: float,
        spacing: float,
        padding_left: float,
        padding_top: float,
        cross_align: str,
        main_align: str,
        layout_solver_cb: Any
    ) -> float:
        rows = []
        current_row = []
        current_row_w = 0.0
        current_row_max_h = 0.0
        
        for child in children:
            child_w = child.width
            child_h = child.height
            
            spacing_gap = spacing if current_row_w > 0 else 0.0
            if current_row_w + child_w + spacing_gap <= avail_w:
                current_row.append(child)
                current_row_w += child_w + spacing_gap
                current_row_max_h = max(current_row_max_h, child_h)
            else:
                if current_row:
                    rows.append((current_row, current_row_w, current_row_max_h))
                current_row = [child]
                current_row_w = child_w
                current_row_max_h = child_h
        if current_row:
            rows.append((current_row, current_row_w, current_row_max_h))
            
        current_y = padding_top
        for row_children, row_w, row_h in rows:
            current_x = padding_left
            if main_align == "center":
                current_x += (avail_w - row_w) / 2.0
            elif main_align == "end":
                current_x += avail_w - row_w
                
            for child in row_children:
                y_offset = AlignmentEngine.align_vertical(row_h, child.height, cross_align, 0.0)
                child.x = current_x
                child.y = current_y + y_offset
                
                # Recurse down layouts
                layout_solver_cb(child, child.width, child.height)
                
                current_x += child.width + spacing
            
            current_y += row_h + spacing
            
        total_height = current_y - (spacing if rows else 0.0)
        return total_height
