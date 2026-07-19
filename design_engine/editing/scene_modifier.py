from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, TextNode, ShapeNode, GroupNode, ComponentNode
from design_engine.editing.models import ParsedIntent

class SceneModifier:
    @staticmethod
    def apply_intent(layout: Layout, intent: ParsedIntent) -> None:
        """
        Alters geometry coordinates, font sizes, and styles on matching layout nodes.
        """
        matched_nodes = []
        
        def traverse(node: Node):
            # Target matching matches node IDs or names
            is_match = (
                intent.target == "all" or
                intent.target in node.id.lower() or
                isinstance(node, TextNode) and intent.target == "text" or
                isinstance(node, ComponentNode) and intent.target == "cta" and ("cta" in node.id.lower() or "button" in node.id.lower())
            )
            if is_match:
                matched_nodes.append(node)
                
            if isinstance(node, GroupNode):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)

        for node in matched_nodes:
            if intent.action == "resize":
                if isinstance(node, TextNode):
                    if "font_size_scale" in intent.properties:
                        node.properties.font_size *= intent.properties["font_size_scale"]
                else:
                    if "width_scale" in intent.properties:
                        node.width *= intent.properties["width_scale"]
                    if "height_scale" in intent.properties:
                        node.height *= intent.properties["height_scale"]
                        
            elif intent.action == "move":
                if "x" in intent.properties:
                    node.x = intent.properties["x"]
                if "y" in intent.properties:
                    node.y = intent.properties["y"]
                if isinstance(node, TextNode) and "align" in intent.properties:
                    node.properties.align = intent.properties["align"]
                elif isinstance(node, GroupNode) and "align" in intent.properties:
                    node.main_align = intent.properties["align"]
                    
            elif intent.action == "style_shift":
                if "border_radius" in intent.properties:
                    if isinstance(node, ShapeNode):
                        node.properties.border_radius = intent.properties["border_radius"]
                
                # Smart style shift for premium/modern
                if intent.properties.get("style") in ("premium", "modern"):
                    if isinstance(node, TextNode):
                        node.properties.font_family = "Georgia" if intent.properties["style"] == "premium" else "Outfit"
                    layout.canvas.background_color = "#1E293B" if intent.properties["style"] == "premium" else "#FFFFFF"
                    
            elif intent.action == "recolor":
                if "color" in intent.properties:
                    if isinstance(node, TextNode):
                        node.properties.color = intent.properties["color"]
                    elif isinstance(node, ShapeNode):
                        node.properties.fill_color = intent.properties["color"]
                        
        # Recoloring target background updates the canvas color directly
        if intent.action == "recolor" and intent.target == "background" and "color" in intent.properties:
            layout.canvas.background_color = intent.properties["color"]
