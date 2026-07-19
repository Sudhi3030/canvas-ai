from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import ShapeNode, ShapeProperties

class DecorationEngine:
    @staticmethod
    def inject_decorations(layout: Layout) -> None:
        """
        Injects abstract decorative shapes into the bottom-most layers of the scene tree.
        """
        # Check idempotency to prevent duplicate injections
        exists = any(node.id == "accent_blob_bg" for node in layout.scene_tree)
        if exists:
            return
            
        w = float(layout.canvas.width)
        
        # Inject abstract background accent shape
        accent_blob = ShapeNode(
            id="accent_blob_bg",
            name="Accent Blob",
            x=w - 150.0,
            y=50.0,
            width=120.0,
            height=120.0,
            opacity=0.15,
            properties=ShapeProperties(
                shape_type="circle",
                fill_color="#D97706",
                stroke_color=None,
                stroke_width=0.0
            )
        )
        
        # Insert at bottom layer (zero)
        layout.scene_tree.insert(0, accent_blob)
