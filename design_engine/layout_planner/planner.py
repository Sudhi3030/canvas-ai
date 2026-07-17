from typing import Dict, Any, Optional
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import GroupNode, ShapeNode, TextNode, ImageNode, ComponentNode, ShadowEffect
from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateSpec
from design_engine.semantic_scene.models import SemanticScene, SemanticNode
from design_engine.layout_engine.layout import LayoutSolver

class LayoutPlanner:
    def __init__(self, solver: LayoutSolver = None):
        self.solver = solver or LayoutSolver()

    def plan_layout(
        self,
        scene: SemanticScene,
        spec: TemplateSpec,
        brand: BrandKit,
        variant_style: Optional[Dict[str, Any]] = None
    ) -> Layout:
        """
        Dynamically compiles a semantic scene description into a concrete layout structure
        applying design guidelines, brand kits, and styling overrides.
        """
        style = variant_style or {}
        
        # 1. Resolve style properties with fallbacks to brand kit
        font_h = style.get("font_heading", brand.font_heading)
        font_b = style.get("font_body", brand.font_body)
        
        bg_color = style.get("bg_color", brand.primary_color)
        card_color = style.get("card_color", brand.secondary_color)
        accent_color = style.get("accent_color", brand.accent_color)
        
        border_radius = style.get("border_radius", brand.border_radius_default)
        spacing_mult = style.get("spacing_scale", brand.spacing_scale)
        shadow = style.get("shadow_preset", brand.shadow_preset)
        gradient = style.get("gradient_preset", brand.gradient_preset)
        
        # Define base platform canvas dimensions
        canvas = Canvas(
            width=spec.width,
            height=spec.height,
            background_color=bg_color,
            unit="px"
        )
        
        # 2. Build Card Background Shape Node
        card_w = float(spec.width - (spec.padding * 2))
        card_h = float(spec.height - (spec.padding * 2))
        
        card_bg_props = {
            "fill_color": card_color,
            "border_radius": border_radius,
            "stroke_color": accent_color,
            "stroke_width": 2
        }
        if gradient:
            card_bg_props["fill_gradient"] = gradient.model_dump() if hasattr(gradient, "model_dump") else gradient
            
        card_bg = ShapeNode(
            id="card_bg",
            name="Card Background Panel",
            x=0, y=0,
            width_policy="fill",
            height_policy="fill",
            z_index=0,
            properties=card_bg_props,
            effects=[shadow] if shadow else []
        )
        
        # 3. Place Semantic elements into Template Slots dynamically
        stack_children = []
        
        # Helper to find matching semantic nodes by template slot type
        def find_semantic_node(slot_type: str) -> Optional[SemanticNode]:
            # Map slot types to matching roles/sections
            for node in scene.elements:
                if slot_type == "logo" and (node.role == "logo_image" or node.section == "logo"):
                    return node
                elif slot_type == "heading" and (node.role == "headline" or node.section == "hero"):
                    return node
                elif slot_type == "body" and (node.role == "description" or node.section == "description"):
                    return node
                elif slot_type == "cta" and (node.role == "button" or node.section == "cta"):
                    return node
                elif slot_type == "hero" and (node.role == "hero_image" or node.section == "product"):
                    return node
            return None

        for slot in spec.slots:
            node = find_semantic_node(slot.type)
            if not node:
                continue
                
            if slot.type == "logo":
                stack_children.append(
                    ImageNode(
                        id=slot.id,
                        name=slot.name,
                        width=120.0,
                        height=120.0,
                        width_policy="fixed",
                        height_policy="fixed",
                        z_index=1,
                        properties={
                            "url": node.content or brand.logo_url or "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80",
                            "fit_mode": "contain"
                        }
                    )
                )
            elif slot.type == "heading":
                # Smart text scaling: high priority headline gets larger size
                base_size = 48.0 if spec.width >= 1000 else 36.0
                if node.priority == "high":
                    base_size *= 1.2
                elif node.priority == "low":
                    base_size *= 0.8
                    
                stack_children.append(
                    TextNode(
                        id=slot.id,
                        name=slot.name,
                        width_policy="fill",
                        height_policy="fit",
                        z_index=2,
                        properties={
                            "content": node.content or "Headline Text",
                            "font_family": font_h,
                            "font_size": base_size,
                            "color": accent_color,
                            "align": "center",
                            "vertical_align": "middle",
                            "letter_spacing": 2.0
                        }
                    )
                )
            elif slot.type == "body":
                base_size = 24.0 if spec.width >= 1000 else 18.0
                if node.priority == "high":
                    base_size *= 1.1
                elif node.priority == "low":
                    base_size *= 0.9
                    
                stack_children.append(
                    TextNode(
                        id=slot.id,
                        name=slot.name,
                        width_policy="fill",
                        height_policy="fit",
                        z_index=3,
                        properties={
                            "content": node.content or "Description copy goes here.",
                            "font_family": font_b,
                            "font_size": base_size,
                            "color": "#F8FAFC",
                            "align": "center",
                            "line_height": 1.5
                        }
                    )
                )
            elif slot.type == "cta":
                # Smart CTA prominence: primary style inherits accent colors and shadow
                btn_border_radius = style.get("button_radius", brand.button_radius)
                
                stack_children.append(
                    ComponentNode(
                        id=slot.id,
                        name=slot.name,
                        width=240.0 if spec.width >= 1000 else 180.0,
                        height=60.0 if spec.width >= 1000 else 48.0,
                        width_policy="fixed",
                        height_policy="fixed",
                        z_index=4,
                        label=node.content or "ORDER NOW",
                        bg_color=accent_color if node.style == "primary" else card_color,
                        text_color=bg_color if node.style == "primary" else accent_color,
                        border_radius=btn_border_radius,
                        effects=[
                            ShadowEffect(
                                type="drop_shadow",
                                color="#000000",
                                offset_x=0.0,
                                offset_y=4.0,
                                blur=8.0
                            )
                        ]
                    )
                )
            elif slot.type == "hero":
                url = node.content or "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&q=80"
                # Smart hero image size: luxury variant uses larger image
                hero_w = 350.0 if spec.width >= 1000 else 250.0
                hero_h = 250.0 if spec.height >= 1000 else 180.0
                if node.priority == "high":
                    hero_h *= 1.2
                    
                stack_children.append(
                    ImageNode(
                        id=slot.id,
                        name=slot.name,
                        width=hero_w,
                        height=hero_h,
                        width_policy="fill",
                        height_policy="fixed",
                        z_index=2,
                        properties={
                            "url": url,
                            "fit_mode": "cover",
                            "border_radius": border_radius
                        }
                    )
                )
                
        # 4. Build Content Flow Stack
        content_stack = GroupNode(
            id="content_stack",
            name="Content Layout Stack",
            x=0, y=0,
            width_policy="fill",
            height_policy="fill",
            layout_mode="vertical",
            spacing=spec.spacing * spacing_mult,
            padding_left=40.0,
            padding_right=40.0,
            padding_top=50.0,
            padding_bottom=50.0,
            cross_align="center",
            main_align="center",
            z_index=1,
            children=stack_children
        )
        
        # Build absolute container group holding background frame and stack children
        container_group = GroupNode(
            id="main_container",
            name="Branded Content Container",
            x=spec.padding,
            y=spec.padding,
            width=card_w,
            height=card_h,
            layout_mode="absolute",
            z_index=1,
            children=[card_bg, content_stack]
        )
        
        metadata = Metadata(
            created_by=f"LayoutPlanner v1.0 ({brand.name})",
            template=spec.name,
            version="1.0"
        )
        
        layout_doc = Layout(
            canvas=canvas,
            scene_tree=[container_group],
            metadata=metadata
        )
        
        # Solve layout positions
        self.solver.solve(layout_doc)
        return layout_doc
