from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import ShapeNode, ShapeProperties

class DecorationGenerator:
    @staticmethod
    def inject_decorations(layout: Layout, style: str, accent_color: str) -> None:
        """
        Injects abstract waves or circles behind content depending on design theme.
        """
        exists = any(node.id == "accent_blob_bg" for node in layout.scene_tree)
        if exists:
            return
            
        w = float(layout.canvas.width)
        
        # Keep minimal designs perfectly clear and free of decorations
        if style.lower() != "minimal":
            accent_blob = ShapeNode(
                id="accent_blob_bg",
                name="Accent Blob",
                x=w - 120.0,
                y=80.0,
                width=100.0,
                height=100.0,
                opacity=0.15,
                properties=ShapeProperties(
                    shape_type="circle",
                    fill_color=accent_color,
                    stroke_color=None,
                    stroke_width=0.0
                )
            )
            layout.scene_tree.insert(0, accent_blob)
