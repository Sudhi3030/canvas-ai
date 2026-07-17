from typing import Dict, Tuple, List, Literal
from PIL import ImageDraw
from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, GroupNode, TextNode, ImageNode, ShapeNode

def wrap_text(content: str, font, max_width: float, letter_spacing: float = 0.0) -> List[str]:
    """
    Wraps text into lines using word measurements and letter-spacing gaps.
    """
    if max_width <= 0:
        return [content]

    def measure_string(s: str) -> float:
        if not s:
            return 0.0
        if letter_spacing > 0:
            return sum(font.getlength(c) for c in s) + letter_spacing * (len(s) - 1)
        return font.getlength(s)

    paragraphs = content.split("\n")
    lines = []

    for para in paragraphs:
        words = para.split(" ")
        current_line = []
        
        for word in words:
            # Check size of line + word
            test_line = " ".join(current_line + [word]) if current_line else word
            if measure_string(test_line) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    # Single word is wider than max_width: force split character by character
                    char_accum = ""
                    for char in word:
                        test_char_line = char_accum + char
                        if measure_string(test_char_line) <= max_width:
                            char_accum = test_char_line
                        else:
                            if char_accum:
                                lines.append(char_accum)
                            char_accum = char
                    if char_accum:
                        current_line = [char_accum]
        if current_line:
            lines.append(" ".join(current_line))
            
    return lines

class LayoutSolver:
    def __init__(self):
        # We need a dummy drawing context to measure text bounds during Phase 1
        from PIL import Image
        self.dummy_img = Image.new("RGBA", (1, 1))
        self.dummy_draw = ImageDraw.Draw(self.dummy_img)

    def solve(self, layout: Layout) -> None:
        """
        Updates coordinate offsets x, y and dimensions width, height of all nodes
        in the scene graph using a two-pass calculation.
        """
        # Pass 1: Measure preferred sizes from bottom-up
        for node in layout.scene_tree:
            self._measure_node(node)

        # Pass 2: Position elements and compute final fill dimensions top-down
        canvas_w = float(layout.canvas.width)
        canvas_h = float(layout.canvas.height)
        
        # Position roots relative to the Canvas boundary context
        for node in layout.scene_tree:
            # If root has fill policy, resolve to canvas size
            if node.width_policy == "fill":
                node.width = canvas_w
            if node.height_policy == "fill":
                node.height = canvas_h
            
            # Recurse layout solver down the tree
            self._layout_node(node, node.width, node.height)

    def _measure_node(self, node: Node) -> Tuple[float, float]:
        """
        Pass 1: Computes the preferred (measured) width and height of the node.
        """
        if not node.visible:
            return 0.0, 0.0

        measured_w = node.width
        measured_h = node.height

        # A. Measure leaves based on content
        if isinstance(node, TextNode):
            from design_engine.renderer.canvas_renderer import load_font
            font = load_font(node.properties.font_family, node.properties.font_size)
            
            # If width_policy is fit, it's a single line of text
            if node.width_policy == "fit":
                text_w = sum(font.getlength(c) for c in node.properties.content) + node.properties.letter_spacing * (len(node.properties.content) - 1)
                measured_w = text_w
                
            # If height_policy is fit, it depends on whether we wrap or not
            if node.height_policy == "fit":
                # If width_policy is fit, it's just one line height
                if node.width_policy == "fit":
                    bbox = self.dummy_draw.textbbox((0, 0), "Ap", font=font)
                    measured_h = (bbox[3] - bbox[1]) * node.properties.line_height
                else:
                    # Wrapped height based on current width (which is fixed/fill)
                    lines = wrap_text(node.properties.content, font, node.width, node.properties.letter_spacing)
                    bbox = self.dummy_draw.textbbox((0, 0), "Ap", font=font)
                    line_h = (bbox[3] - bbox[1])
                    measured_h = len(lines) * line_h * node.properties.line_height
                    
        # B. Measure groups based on layout flow direction
        elif isinstance(node, GroupNode):
            # Recurse children measurements first
            children_sizes = [self._measure_node(child) for child in node.children]
            
            if node.layout_mode in ("horizontal", "vertical"):
                inner_w = 0.0
                inner_h = 0.0
                num_children = len(node.children)
                
                if num_children > 0:
                    spacing_total = node.spacing * (num_children - 1)
                    
                    if node.layout_mode == "vertical":
                        inner_h = sum(h for _, h in children_sizes) + spacing_total
                        inner_w = max((w for w, _ in children_sizes), default=0.0)
                    else:  # horizontal
                        inner_w = sum(w for w, _ in children_sizes) + spacing_total
                        inner_h = max((h for _, h in children_sizes), default=0.0)

                # Add padding to measurements
                measured_w_flow = inner_w + node.padding_left + node.padding_right
                measured_h_flow = inner_h + node.padding_top + node.padding_bottom
                
                if node.width_policy == "fit":
                    measured_w = measured_w_flow
                if node.height_policy == "fit":
                    measured_h = measured_h_flow
            else:
                # Absolute group matches explicit size or bounds
                pass

        # Update node internal states
        node.width = measured_w
        node.height = measured_h
        return measured_w, measured_h

    def _layout_node(self, node: Node, concrete_w: float, concrete_h: float) -> None:
        """
        Pass 2: Computes relative offsets and sizes for child elements.
        """
        # Dynamic re-measure for TextNodes with fit height once width is concrete
        if isinstance(node, TextNode) and node.height_policy == "fit":
            from design_engine.renderer.canvas_renderer import load_font
            font = load_font(node.properties.font_family, node.properties.font_size)
            lines = wrap_text(node.properties.content, font, concrete_w, node.properties.letter_spacing)
            bbox = self.dummy_draw.textbbox((0, 0), "Ap", font=font)
            line_h = (bbox[3] - bbox[1])
            concrete_h = len(lines) * line_h * node.properties.line_height

        node.width = concrete_w
        node.height = concrete_h

        if not isinstance(node, GroupNode) or len(node.children) == 0:
            return

        layout_mode = node.layout_mode
        children = node.children
        num_children = len(children)

        # A. Resolve absolute layouts
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

        # B. Resolve stacks (horizontal / vertical flow layouts)
        # Compute bounds minus padding
        avail_w = concrete_w - (node.padding_left + node.padding_right)
        avail_h = concrete_h - (node.padding_top + node.padding_bottom)
        
        spacing_total = node.spacing * (num_children - 1)

        # 1. Distribute flex sizes (fill)
        # Calculate how much space is absorbed by fixed and fit children
        flex_count = 0
        allocated_main = 0.0

        for child in children:
            if layout_mode == "vertical":
                if child.height_policy == "fill":
                    flex_count += 1
                else:
                    allocated_main += child.height
            else:  # horizontal
                if child.width_policy == "fill":
                    flex_count += 1
                else:
                    allocated_main += child.width

        remaining_main = (avail_h if layout_mode == "vertical" else avail_w) - allocated_main - spacing_total
        flex_unit_size = max(0.0, remaining_main / flex_count) if flex_count > 0 else 0.0

        # 2. Position stack flow
        current_offset = node.padding_top if layout_mode == "vertical" else node.padding_left

        # Adjust start offset if justified to center or end
        total_flow_size = allocated_main + spacing_total + (flex_count * flex_unit_size)
        if node.main_align == "center":
            diff = (avail_h if layout_mode == "vertical" else avail_w) - total_flow_size
            if diff > 0:
                current_offset += diff / 2
        elif node.main_align == "end":
            diff = (avail_h if layout_mode == "vertical" else avail_w) - total_flow_size
            if diff > 0:
                current_offset += diff

        for child in children:
            # Resolve width/height constraints
            child_w = child.width
            child_h = child.height

            if layout_mode == "vertical":
                # Handle Main Axis (Vertical)
                if child.height_policy == "fill":
                    child_h = flex_unit_size
                
                # Handle Cross Axis (Horizontal)
                if child.width_policy == "fill" or node.cross_align == "stretch":
                    child_w = avail_w
                
                # Apply cross alignment positioning offset
                cross_offset = node.padding_left
                if node.cross_align == "center" and child.width_policy != "fill":
                    cross_offset += (avail_w - child_w) / 2
                elif node.cross_align == "end" and child.width_policy != "fill":
                    cross_offset += avail_w - child_w

                child.x = cross_offset
                child.y = current_offset
                
                self._layout_node(child, child_w, child_h)
                current_offset += child_h + node.spacing

            else:  # horizontal
                # Handle Main Axis (Horizontal)
                if child.width_policy == "fill":
                    child_w = flex_unit_size
                
                # Handle Cross Axis (Vertical)
                if child.height_policy == "fill" or node.cross_align == "stretch":
                    child_h = avail_h
                
                # Apply cross alignment positioning offset
                cross_offset = node.padding_top
                if node.cross_align == "center" and child.height_policy != "fill":
                    cross_offset += (avail_h - child_h) / 2
                elif node.cross_align == "end" and child.height_policy != "fill":
                    cross_offset += avail_h - child_h

                child.x = current_offset
                child.y = cross_offset
                
                self._layout_node(child, child_w, child_h)
                current_offset += child_w + node.spacing
