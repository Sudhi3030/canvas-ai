from typing import List, Any

class GridSolver:
    @staticmethod
    def solve_grid(
        children: List[Any],
        avail_w: float,
        avail_h: float,
        columns_count: int,
        spacing: float,
        padding_left: float,
        padding_top: float,
        layout_solver_cb: Any
    ) -> float:
        """Positions children inside cells in a columns matrix."""
        if columns_count <= 0:
            columns_count = 2
        
        col_w = (avail_w - spacing * (columns_count - 1)) / columns_count
        row_h = 100.0 # Default grid cell row height
        
        for idx, child in enumerate(children):
            col_idx = idx % columns_count
            row_idx = idx // columns_count
            
            x = padding_left + col_idx * (col_w + spacing)
            y = padding_top + row_idx * (row_h + spacing)
            
            child.x = x
            child.y = y
            child.width = col_w
            child.height = row_h
            
            # Recurse down layouts
            layout_solver_cb(child, col_w, row_h)
            
        rows_count = (len(children) + columns_count - 1) // columns_count
        total_height = padding_top + rows_count * (row_h + spacing) - (spacing if rows_count > 0 else 0.0)
        return total_height
