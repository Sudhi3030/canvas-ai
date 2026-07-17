from typing import List, Tuple
from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, TextNode, ShapeNode, GroupNode, ComponentNode
from design_engine.design_rules.accessibility import contrast_ratio

class LayoutScorer:
    def score(self, layout: Layout) -> float:
        """
        Heuristically scores a layout from 0.0 to 100.0 based on visual quality.
        """
        score = 100.0
        
        # 1. Flatten visual nodes and get bounding boxes
        nodes = []
        def collect_nodes(node: Node, parent_x: float, parent_y: float):
            # Create a simplified list holding resolved coordinates
            if not node.visible:
                return
            world_x = parent_x + node.x
            world_y = parent_y + node.y
            
            if isinstance(node, GroupNode):
                for child in node.children:
                    collect_nodes(child, world_x, world_y)
            else:
                nodes.append((node, world_x, world_y))
                
        for root in layout.scene_tree:
            collect_nodes(root, 0.0, 0.0)
            
        # A. Overlap Deductions (up to 30 pts)
        overlaps = 0
        for i in range(len(nodes)):
            n1, x1, y1 = nodes[i]
            for j in range(i + 1, len(nodes)):
                n2, x2, y2 = nodes[j]
                if n1.z_index == 0 or n2.z_index == 0 or "bg" in n1.id or "bg" in n2.id:
                    continue
                # AABB check
                overlap = not (x1 + n1.width <= x2 or
                               x2 + n2.width <= x1 or
                               y1 + n1.height <= y2 or
                               y2 + n2.height <= y1)
                if overlap:
                    overlaps += 1
                    
        if overlaps > 0:
            score -= min(30.0, overlaps * 15.0)

        # B. Typographic Hierarchy Deductions (up to 20 pts)
        headings = [n for n, _, _ in nodes if isinstance(n, TextNode) and ("heading" in n.id.lower() or "title" in n.id.lower() or "heading" in n.name.lower() or "title" in n.name.lower())]
        bodies = [n for n, _, _ in nodes if isinstance(n, TextNode) and ("body" in n.id.lower() or "desc" in n.id.lower() or "copy" in n.id.lower() or "body" in n.name.lower() or "desc" in n.name.lower())]
        
        for h in headings:
            for b in bodies:
                if h.properties.font_size < b.properties.font_size * 1.5:
                    score -= 20.0
                    break

        # C. Whitespace Density Deductions (up to 15 pts)
        canvas_area = float(layout.canvas.width * layout.canvas.height)
        element_area = 0.0
        for n, _, _ in nodes:
            if n.z_index > 0 and "bg" not in n.id:
                element_area += float(n.width * n.height)
                
        fill_ratio = element_area / canvas_area
        if fill_ratio < 0.20 or fill_ratio > 0.65:
            score -= 15.0

        # D. Contrast Deductions (up to 15 pts)
        canvas_bg = layout.canvas.background_color
        for n, _, _ in nodes:
            if isinstance(n, TextNode):
                ratio = contrast_ratio(n.properties.color, canvas_bg)
                required = 3.0 if n.properties.font_size >= 18.0 else 4.5
                if ratio < required:
                    score -= 7.5

        # E. CTA Presence & Visibility (up to 20 pts)
        ctas = [n for n, _, _ in nodes if isinstance(n, ComponentNode) and ("cta" in n.id.lower() or "button" in n.id.lower())]
        if not ctas:
            score -= 20.0
        else:
            for cta in ctas:
                if not cta.visible or cta.opacity < 0.8:
                    score -= 10.0

        # F. Legibility Size Check (up to 10 pts)
        for n, _, _ in nodes:
            if isinstance(n, TextNode) and n.properties.font_size < 10.0:
                score -= 10.0
                break

        return max(0.0, score)
