from typing import List, Any
from design_engine.layout_engine.alignment import AlignmentEngine

class StackSolver:
    @staticmethod
    def solve_vertical(
        children: List[Any],
        avail_w: float,
        avail_h: float,
        spacing: float,
        padding_left: float,
        padding_top: float,
        cross_align: str,
        main_align: str,
        layout_solver_cb: Any
    ) -> float:
        spacing_total = spacing * (len(children) - 1) if children else 0.0
        allocated_main = sum(c.height for c in children if c.height_policy != "fill")
        flex_count = sum(1 for c in children if c.height_policy == "fill")
        
        remaining_main = avail_h - allocated_main - spacing_total
        flex_unit = max(0.0, remaining_main / flex_count) if flex_count > 0 else 0.0
        
        current_y = padding_top
        total_size = allocated_main + spacing_total + (flex_count * flex_unit)
        
        if main_align == "center" and remaining_main > 0 and flex_count == 0:
            current_y += remaining_main / 2.0
        elif main_align == "end" and remaining_main > 0 and flex_count == 0:
            current_y += remaining_main

        for child in children:
            if child.height_policy == "fill":
                child_h = flex_unit
            else:
                child_h = child.height

            if child.width_policy == "fill" or cross_align == "stretch":
                child_w = avail_w
            else:
                child_w = child.width

            child_x = AlignmentEngine.align_horizontal(avail_w, child_w, cross_align, padding_left)
            child.x = child_x
            child.y = current_y
            
            # Recurse down layouts
            layout_solver_cb(child, child_w, child_h)
            
            current_y += child_h + spacing
            
        return total_size

    @staticmethod
    def solve_horizontal(
        children: List[Any],
        avail_w: float,
        avail_h: float,
        spacing: float,
        padding_left: float,
        padding_top: float,
        cross_align: str,
        main_align: str,
        layout_solver_cb: Any
    ) -> float:
        spacing_total = spacing * (len(children) - 1) if children else 0.0
        allocated_main = sum(c.width for c in children if c.width_policy != "fill")
        flex_count = sum(1 for c in children if c.width_policy == "fill")
        
        remaining_main = avail_w - allocated_main - spacing_total
        flex_unit = max(0.0, remaining_main / flex_count) if flex_count > 0 else 0.0
        
        current_x = padding_left
        total_size = allocated_main + spacing_total + (flex_count * flex_unit)
        
        if main_align == "center" and remaining_main > 0 and flex_count == 0:
            current_x += remaining_main / 2.0
        elif main_align == "end" and remaining_main > 0 and flex_count == 0:
            current_x += remaining_main

        for child in children:
            if child.width_policy == "fill":
                child_w = flex_unit
            else:
                child_w = child.width

            if child.height_policy == "fill" or cross_align == "stretch":
                child_h = avail_h
            else:
                child_h = child.height

            child_y = AlignmentEngine.align_vertical(avail_h, child_h, cross_align, padding_top)
            child.x = current_x
            child.y = child_y
            
            # Recurse down layouts
            layout_solver_cb(child, child_w, child_h)
            
            current_x += child_w + spacing
            
        return total_size
