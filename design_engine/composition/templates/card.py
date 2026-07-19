from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import GroupNode, ShapeNode, TextNode, ImageNode, ComponentNode, ShapeProperties
from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateSpec

class CardTemplate:
    @staticmethod
    def build(spec: TemplateSpec, brand: BrandKit, logo: str, heading: str, body: str, cta: str, hero_url: str) -> Layout:
        canvas = Canvas(width=spec.width, height=spec.height, background_color="#FFFFFF")
        
        # Central card occupying 85% of dimensions
        card_w = float(spec.width) * 0.85
        card_h = float(spec.height) * 0.85
        card_x = (float(spec.width) - card_w) / 2.0
        card_y = (float(spec.height) - card_h) / 2.0
        
        card_bg = ShapeNode(id="card_bg", name="Card BG", x=0, y=0, width=card_w, height=card_h, z_index=0, properties=ShapeProperties(border_radius=16.0))
        
        logo_node = ImageNode(id="logo", name="Logo", width=80.0, height=80.0, width_policy="fixed", height_policy="fixed", z_index=1, properties={"url": logo, "fit_mode": "contain"})
        headline_node = TextNode(id="heading", name="Headline", width_policy="fill", height_policy="fit", z_index=2, properties={"content": heading, "font_family": "Arial", "font_size": 36.0, "color": "#000000", "align": "center"})
        
        hero_node = ImageNode(id="hero", name="Hero Image", width=float(card_w - 60), height=float(card_h * 0.35), width_policy="fixed", height_policy="fixed", z_index=2, properties={"url": hero_url, "fit_mode": "cover"})
        body_node = TextNode(id="body", name="Description", width_policy="fill", height_policy="fit", z_index=3, properties={"content": body, "font_family": "Arial", "font_size": 18.0, "color": "#475569", "align": "center"})
        cta_node = ComponentNode(id="cta", name="CTA Button", width=220.0, height=55.0, width_policy="fixed", height_policy="fixed", z_index=4, label=cta)
        
        content_stack = GroupNode(
            id="content_stack", name="Content Stack", x=0, y=0, width=card_w, height=card_h,
            layout_mode="vertical", spacing=15.0, padding_left=20.0, padding_right=20.0, padding_top=20.0, padding_bottom=20.0,
            cross_align="center", main_align="center", z_index=1,
            children=[logo_node, headline_node, hero_node, body_node, cta_node]
        )
        
        container_group = GroupNode(
            id="main_container", name="Branded Container", x=card_x, y=card_y,
            width=card_w, height=card_h,
            layout_mode="absolute", z_index=1, children=[card_bg, content_stack]
        )
        return Layout(canvas=canvas, scene_tree=[container_group], metadata=Metadata(created_by="CompositionEngine", template=spec.name, version="1.0"))
