import logging
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import GroupNode, ShapeNode, TextNode, ImageNode
from design_engine.brand.brand_kit import BrandKit

logger = logging.getLogger("TemplateEngine")

class TemplateSlot(BaseModel):
    id: str
    name: str
    type: Literal["logo", "heading", "body", "cta", "hero", "footer"]
    width_policy: str = "fill"
    height_policy: str = "fit"

class TemplateSpec(BaseModel):
    name: str
    width: int
    height: int
    padding: float
    spacing: float
    slots: List[TemplateSlot] = Field(default_factory=list)

TEMPLATES: Dict[str, TemplateSpec] = {
    "Instagram": TemplateSpec(
        name="Instagram",
        width=1080, height=1080,
        padding=60.0, spacing=40.0,
        slots=[
            TemplateSlot(id="brand_logo", name="Logo Slot", type="logo"),
            TemplateSlot(id="header_text", name="Heading Slot", type="heading"),
            TemplateSlot(id="body_text", name="Body Slot", type="body"),
            TemplateSlot(id="cta_button", name="CTA Button Slot", type="cta")
        ]
    ),
    "Facebook": TemplateSpec(
        name="Facebook",
        width=1200, height=630,
        padding=40.0, spacing=30.0,
        slots=[
            TemplateSlot(id="brand_logo", name="Logo Slot", type="logo"),
            TemplateSlot(id="header_text", name="Heading Slot", type="heading"),
            TemplateSlot(id="body_text", name="Body Slot", type="body"),
            TemplateSlot(id="cta_button", name="CTA Button Slot", type="cta")
        ]
    ),
    "Pinterest": TemplateSpec(
        name="Pinterest",
        width=1000, height=1500,
        padding=80.0, spacing=50.0,
        slots=[
            TemplateSlot(id="header_text", name="Heading Slot", type="heading"),
            TemplateSlot(id="hero_image", name="Hero Slot", type="hero"),
            TemplateSlot(id="body_text", name="Body Slot", type="body"),
            TemplateSlot(id="cta_button", name="CTA Button Slot", type="cta")
        ]
    ),
    "Story": TemplateSpec(
        name="Story",
        width=1080, height=1920,
        padding=80.0, spacing=60.0,
        slots=[
            TemplateSlot(id="brand_logo", name="Logo Slot", type="logo"),
            TemplateSlot(id="header_text", name="Heading Slot", type="heading"),
            TemplateSlot(id="body_text", name="Body Slot", type="body"),
            TemplateSlot(id="cta_button", name="CTA Button Slot", type="cta")
        ]
    )
}

class TemplateEngine:
    @staticmethod
    def create_branded_layout(
        template_name: str,
        brand: BrandKit,
        heading_text: str,
        body_text: str,
        hero_image_url: Optional[str] = None
    ) -> Layout:
        """
        Generates a structured, validated, and brand-consistent design layout
        matching the target platform.
        """
        spec = TEMPLATES.get(template_name)
        if not spec:
            logger.warning(f"Unknown template '{template_name}'. Falling back to Instagram square.")
            spec = TEMPLATES["Instagram"]

        # 1. Setup Canvas matching brand primary theme
        canvas = Canvas(
            width=spec.width,
            height=spec.height,
            background_color=brand.primary_color,
            unit="px"
        )

        # 2. Build Card Background Panel
        card_w = float(spec.width - (spec.padding * 2))
        card_h = float(spec.height - (spec.padding * 2))

        card_bg = ShapeNode(
            id="card_bg",
            name="Card Background Panel",
            x=0, y=0,
            width_policy="fill",
            height_policy="fill",
            z_index=0,
            properties={
                "fill_color": brand.secondary_color,
                "border_radius": brand.border_radius_default,
                "stroke_color": brand.accent_color,
                "stroke_width": 2
            },
            effects=[brand.shadow_preset] if brand.shadow_preset else []
        )

        # 3. Populate Slots dynamically
        from design_engine.scene_graph.node import ComponentNode, ShadowEffect
        stack_children = []

        for slot in spec.slots:
            if slot.type == "logo":
                if brand.logo_url:
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
                                "url": brand.logo_url,
                                "fit_mode": "contain"
                            }
                        )
                    )
            elif slot.type == "heading":
                stack_children.append(
                    TextNode(
                        id=slot.id,
                        name=slot.name,
                        width_policy="fill",
                        height_policy="fit",
                        z_index=2,
                        properties={
                            "content": heading_text,
                            "font_family": brand.font_heading,
                            "font_size": 48.0 if spec.width >= 1000 else 36.0,
                            "color": brand.accent_color,
                            "align": "center",
                            "vertical_align": "middle",
                            "letter_spacing": 2.0
                        }
                    )
                )
            elif slot.type == "body":
                stack_children.append(
                    TextNode(
                        id=slot.id,
                        name=slot.name,
                        width_policy="fill",
                        height_policy="fit",
                        z_index=3,
                        properties={
                            "content": body_text,
                            "font_family": brand.font_body,
                            "font_size": 24.0 if spec.width >= 1000 else 18.0,
                            "color": "#F8FAFC",
                            "align": "center",
                            "line_height": 1.5
                        }
                    )
                )
            elif slot.type == "cta":
                stack_children.append(
                    ComponentNode(
                        id=slot.id,
                        name=slot.name,
                        width=240.0 if spec.width >= 1000 else 180.0,
                        height=60.0 if spec.width >= 1000 else 48.0,
                        width_policy="fixed",
                        height_policy="fixed",
                        z_index=4,
                        label="ORDER NOW",
                        bg_color=brand.accent_color,
                        text_color=brand.primary_color,
                        border_radius=brand.button_radius,
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
                url = hero_image_url or "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&q=80"
                stack_children.append(
                    ImageNode(
                        id=slot.id,
                        name=slot.name,
                        width=350.0 if spec.width >= 1000 else 250.0,
                        height=250.0 if spec.height >= 1000 else 180.0,
                        width_policy="fill",
                        height_policy="fixed",
                        z_index=2,
                        properties={
                            "url": url,
                            "fit_mode": "cover",
                            "border_radius": brand.border_radius_default
                        }
                    )
                )

        # Build Content Stack (which layout engine flows vertically)
        content_stack = GroupNode(
            id="content_stack",
            name="Content Layout Stack",
            x=0, y=0,
            width_policy="fill",
            height_policy="fill",
            layout_mode="vertical",
            spacing=spec.spacing * brand.spacing_scale,
            padding_left=40.0,
            padding_right=40.0,
            padding_top=50.0,
            padding_bottom=50.0,
            cross_align="center",
            main_align="center",
            z_index=1,
            children=stack_children
        )

        # Build Container Group Node (holds the background shape and the content flow stack)
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

        # 4. Compile layout envelope
        metadata = Metadata(
            created_by=f"TemplateEngine v1.0 ({brand.name})",
            template=template_name,
            version="1.0"
        )

        return Layout(
            canvas=canvas,
            scene_tree=[container_group],
            metadata=metadata
        )
