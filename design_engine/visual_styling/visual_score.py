from design_engine.scene_graph.document import Layout

class VisualScorer:
    @staticmethod
    def evaluate_aesthetic_quality(layout: Layout) -> float:
        """
        Gives a visual aesthetic score rating (0-100) based on style properties.
        """
        score = 80.0
        
        # Reward layouts containing background panels or shapes (visual richness)
        has_decoration = any(node.id == "accent_blob_bg" for node in layout.scene_tree)
        if has_decoration:
            score += 10.0
            
        # Reward elegant font styles
        def check_text(node) -> bool:
            if hasattr(node, "properties") and node.properties is not None:
                if hasattr(node.properties, "font_family") and node.properties.font_family in ("Georgia", "Times New Roman"):
                    return True
            if hasattr(node, "children"):
                return any(check_text(c) for c in node.children)
            return False

        for root in layout.scene_tree:
            if check_text(root):
                score += 5.0
                break
                
        return min(100.0, score)
