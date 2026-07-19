from typing import Tuple
from PIL import ImageDraw
from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, GroupNode, TextNode

class LayoutSolver:
    def __init__(self):
        from PIL import Image
        self.dummy_img = Image.new("RGBA", (1, 1))
        self.dummy_draw = ImageDraw.Draw(self.dummy_img)

    def solve(self, layout: Layout) -> None:
        """
        Runs the refined 10-pass layout solver pipeline.
        """
        is_template = (layout.metadata is not None and 
                       getattr(layout.metadata, "template", None) is not None and
                       layout.metadata.template != "")
                       
        if is_template:
            # Pass 1: Visual Hierarchy Engine
            from design_engine.layout_engine.visual_hierarchy import VisualHierarchyEngine
            VisualHierarchyEngine.assign_hierarchy_importance(layout)
            
            # Pass 2: Composition Planner
            from design_engine.layout_engine.composition_planner import CompositionPlanner
            strategy = CompositionPlanner.plan_composition(layout)
            
            # Pass 3: Region Generator
            from design_engine.layout_engine.region_generator import RegionGenerator
            RegionGenerator.allocate_regions(layout, strategy)
            
            # Pass 4: Element Sizer (sets dimensions before coordinate solver)
            from design_engine.layout_engine.element_sizer import ElementSizer
            ElementSizer.size_elements(layout)
            
            # Pass 5: Constraint Solver (Initial coordinate constraint solve)
            from design_engine.layout_engine.constraint_solver import ConstraintSolver
            ConstraintSolver.solve_constraints(layout)
            
            # Pass 6: Alignment Engine
            from design_engine.layout_engine.alignment_engine import AlignmentEngine
            AlignmentEngine.align_elements(layout, strategy)
            
            # Pass 7: Spacing Optimizer
            from design_engine.layout_engine.spacing_optimizer import SpacingOptimizer
            SpacingOptimizer.optimize_spacing(layout)
            
            # Pass 8: Collision Detector (passive audit validator)
            from design_engine.layout_engine.collision_detector import CollisionDetector
            conflicts = CollisionDetector.detect_collisions(layout)
            
            # Pass 9: Metrics Engine
            from design_engine.layout_engine.metrics import MetricsEngine
            MetricsEngine.compute_metrics(layout)
            
            # Pass 10: Debug Renderer overlays
            from design_engine.layout_engine.debug_renderer import DebugRenderer
            DebugRenderer.render_debug_overlays(layout)

        # Standard baseline measurements resolver pass
        self._solve_geometry(layout)

    def _solve_geometry(self, layout: Layout) -> None:
        """Computes coordinates & sizes for nodes."""
        for node in layout.scene_tree:
            self._measure_node(node)

        canvas_w = float(layout.canvas.width)
        canvas_h = float(layout.canvas.height)
        
        for node in layout.scene_tree:
            if node.width_policy == "fill":
                node.width = canvas_w
            if node.height_policy == "fill":
                node.height = canvas_h
            self._layout_node(node, node.width, node.height)

    def _measure_node(self, node: Node) -> Tuple[float, float]:
        if not node.visible:
            return 0.0, 0.0

        measured_w = node.width
        measured_h = node.height

        if isinstance(node, TextNode):
            from design_engine.assets.manager import AssetManager
            from design_engine.typography.layout import TypographyEngine
            manager = AssetManager()
            
            if node.width_policy == "fit":
                font = manager.load_font(node.properties.font_family, node.properties.font_size)
                text_w = sum(font.getlength(c) for c in node.properties.content)
                text_w += node.properties.letter_spacing * (len(node.properties.content) - 1)
                words = node.properties.content.split(" ")
                text_w += node.properties.word_spacing * (len(words) - 1)
                measured_w = text_w
                
            if node.height_policy == "fit":
                res = TypographyEngine.layout_text(
                    content=node.properties.content,
                    font_family=node.properties.font_family,
                    font_size=node.properties.font_size,
                    width=measured_w if node.width_policy == "fit" else node.width,
                    height=0.0,
                    line_height=node.properties.line_height,
                    letter_spacing=node.properties.letter_spacing,
                    align=node.properties.align,
                    vertical_align=node.properties.vertical_align,
                    asset_manager=manager,
                    word_spacing=node.properties.word_spacing,
                    paragraph_spacing=node.properties.paragraph_spacing
                )
                if res["lines"]:
                    measured_h = sum(line["height"] for line in res["lines"]) + node.properties.paragraph_spacing * (len(res["lines"]) - 1)
                else:
                    measured_h = 0.0
                    
        elif isinstance(node, GroupNode):
            children_sizes = [self._measure_node(child) for child in node.children]
            num_children = len(node.children)
            inner_w = 0.0
            inner_h = 0.0
            
            if num_children > 0:
                if node.layout_mode == "vertical":
                    spacing_total = node.spacing * (num_children - 1)
                    inner_h = sum(h for _, h in children_sizes) + spacing_total
                    inner_w = max((w for w, _ in children_sizes), default=0.0)
                elif node.layout_mode == "horizontal":
                    spacing_total = node.spacing * (num_children - 1)
                    inner_w = sum(w for w, _ in children_sizes) + spacing_total
                    inner_h = max((h for _, h in children_sizes), default=0.0)
                elif node.layout_mode == "wrap":
                    avail_w = node.width - (node.padding_left + node.padding_right)
                    if node.width_policy == "fit":
                        inner_w = sum(w for w, _ in children_sizes) + node.spacing * (num_children - 1)
                        inner_h = max((h for _, h in children_sizes), default=0.0)
                    else:
                        rows_heights = []
                        current_row_w = 0.0
                        current_row_max_h = 0.0
                        for child_w, child_h in children_sizes:
                            spacing_gap = node.spacing if current_row_w > 0 else 0.0
                            if current_row_w + child_w + spacing_gap <= avail_w:
                                current_row_w += child_w + spacing_gap
                                current_row_max_h = max(current_row_max_h, child_h)
                            else:
                                if current_row_max_h > 0:
                                    rows_heights.append(current_row_max_h)
                                current_row_w = child_w
                                current_row_max_h = child_h
                        if current_row_max_h > 0:
                             rows_heights.append(current_row_max_h)
                        inner_w = avail_w
                        inner_h = sum(rows_heights) + node.spacing * (len(rows_heights) - 1)
                elif node.layout_mode == "grid":
                    columns_count = 2
                    avail_w = node.width - (node.padding_left + node.padding_right)
                    col_w = (avail_w - node.spacing * (columns_count - 1)) / columns_count
                    row_h = 100.0
                    rows_count = (num_children + columns_count - 1) // columns_count
                    inner_w = avail_w
                    inner_h = rows_count * (row_h + node.spacing) - (node.spacing if rows_count > 0 else 0.0)

            measured_w_flow = inner_w + node.padding_left + node.padding_right
            measured_h_flow = inner_h + node.padding_top + node.padding_bottom
            
            if node.width_policy == "fit":
                measured_w = measured_w_flow
            if node.height_policy == "fit":
                measured_h = measured_h_flow

        from design_engine.layout_engine.constraints import ConstraintSolver
        measured_w, measured_h = ConstraintSolver.apply_aspect_ratio(
            measured_w, measured_h, node.aspect_ratio, node.width_policy, node.height_policy
        )

        node.width = measured_w
        node.height = measured_h
        return measured_w, measured_h

    def _layout_node(self, node: Node, concrete_w: float, concrete_h: float) -> None:
        if isinstance(node, TextNode) and node.height_policy == "fit":
            from design_engine.assets.manager import AssetManager
            from design_engine.typography.layout import TypographyEngine
            manager = AssetManager()
            res = TypographyEngine.layout_text(
                content=node.properties.content,
                font_family=node.properties.font_family,
                font_size=node.properties.font_size,
                width=concrete_w,
                height=0.0,
                line_height=node.properties.line_height,
                letter_spacing=node.properties.letter_spacing,
                align=node.properties.align,
                vertical_align=node.properties.vertical_align,
                asset_manager=manager,
                word_spacing=node.properties.word_spacing,
                paragraph_spacing=node.properties.paragraph_spacing
            )
            if res["lines"]:
                concrete_h = sum(line["height"] for line in res["lines"]) + node.properties.paragraph_spacing * (len(res["lines"]) - 1)
            else:
                concrete_h = 0.0

        from design_engine.layout_engine.constraints import ConstraintSolver
        concrete_w, concrete_h = ConstraintSolver.apply_aspect_ratio(
            concrete_w, concrete_h, node.aspect_ratio, node.width_policy, node.height_policy
        )

        node.width = concrete_w
        node.height = concrete_h

        if not isinstance(node, GroupNode) or len(node.children) == 0:
            return

        layout_mode = node.layout_mode
        children = node.children

        if layout_mode == "absolute":
            for child in children:
                child_w = child.width
                child_h = child.height
                if child.width_policy == "fill":
                    child_w = concrete_w
                if child.height_policy == "fill":
                    child_h = concrete_h
                self._layout_node(child, child_w, child_h)
            return

        elif layout_mode == "wrap":
            from design_engine.layout_engine.flex import FlexSolver
            avail_w = concrete_w - (node.padding_left + node.padding_right)
            FlexSolver.solve_wrap(
                children=children,
                avail_w=avail_w,
                spacing=node.spacing,
                padding_left=node.padding_left,
                padding_top=node.padding_top,
                cross_align=node.cross_align,
                main_align=node.main_align,
                layout_solver_cb=self._layout_node
            )
            return

        elif layout_mode == "grid":
            from design_engine.layout_engine.grid import GridSolver
            avail_w = concrete_w - (node.padding_left + node.padding_right)
            avail_h = concrete_h - (node.padding_top + node.padding_bottom)
            GridSolver.solve_grid(
                children=children,
                avail_w=avail_w,
                avail_h=avail_h,
                columns_count=2,
                spacing=node.spacing,
                padding_left=node.padding_left,
                padding_top=node.padding_top,
                layout_solver_cb=self._layout_node
            )
            return

        avail_w = concrete_w - (node.padding_left + node.padding_right)
        avail_h = concrete_h - (node.padding_top + node.padding_bottom)
        
        from design_engine.layout_engine.stack import StackSolver
        if layout_mode == "vertical":
            StackSolver.solve_vertical(
                children=children,
                avail_w=avail_w,
                avail_h=avail_h,
                spacing=node.spacing,
                padding_left=node.padding_left,
                padding_top=node.padding_top,
                cross_align=node.cross_align,
                main_align=node.main_align,
                layout_solver_cb=self._layout_node
            )
        elif layout_mode == "horizontal":
            StackSolver.solve_horizontal(
                children=children,
                avail_w=avail_w,
                avail_h=avail_h,
                spacing=node.spacing,
                padding_left=node.padding_left,
                padding_top=node.padding_top,
                cross_align=node.cross_align,
                main_align=node.main_align,
                layout_solver_cb=self._layout_node
            )

def wrap_text(content: str, font, max_width: float, letter_spacing: float = 0.0) -> list[str]:
    """Backward compatible wrapper delegating to TypographyEngine."""
    from design_engine.typography.layout import TypographyEngine
    return TypographyEngine._wrap_lines(content, font, max_width, letter_spacing, 0.0)
