from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import GroupNode, ShapeNode, TextNode, ImageNode, ComponentNode, ShapeProperties
from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateSpec

class SplitTemplate:
    @staticmethod
    def build(spec: TemplateSpec, brand: BrandKit, logo: str, heading: str, body: str, cta: str, hero_url: str) -> Layout:
        canvas = Canvas(width=spec.width, height=spec.height, background_color="#FFFFFF")
        card_bg = ShapeNode(id="card_bg", name="Card BG", x=0, y=0, width_policy="fill", height_policy="fill", z_index=0, properties=ShapeProperties())
        
        logo_node = ImageNode(id="logo", name="Logo", width=80.0, height=80.0, width_policy="fixed", height_policy="fixed", z_index=1, properties={"url": logo, "fit_mode": "contain"})
        headline_node = TextNode(id="heading", name="Headline", width_policy="fill", height_policy="fit", z_index=2, properties={"content": heading, "font_family": "Arial", "font_size": 36.0, "color": "#000000", "align": "left"})
        body_node = TextNode(id="body", name="Description", width_policy="fill", height_policy="fit", z_index=3, properties={"content": body, "font_family": "Arial", "font_size": 18.0, "color": "#475569", "align": "left"})
        cta_node = ComponentNode(id="cta", name="CTA Button", width=200.0, height=50.0, width_policy="fixed", height_policy="fixed", z_index=4, label=cta)
        
        # Left Text stack
        text_stack = GroupNode(
            id="text_stack", name="Text Stack", x=0, y=0, width=float(spec.width / 2 - 60), height_policy="fill",
            layout_mode="vertical", spacing=15.0, padding_left=20.0, padding_right=20.0, padding_top=40.0, padding_bottom=40.0,
            cross_align="start", main_align="center", z_index=1,
            children=[logo_node, headline_node, body_node, cta_node]
        )
        
        # Right Image takes up full height, remaining width
        hero_w = float(spec.width / 2 - 20)
        hero_node = ImageNode(id="hero", name="Hero Image", width=hero_w, height_policy="fill", z_index=2, properties={"url": hero_url, "fit_mode": "cover"})
        
        content_stack = GroupNode(
            id="content_stack", name="Content Stack", x=0, y=0, width_policy="fill", height_policy="fill",
            layout_mode="horizontal", spacing=20.0, padding_left=20.0, padding_right=20.0, padding_top=20.0, padding_bottom=20.0,
            cross_align="center", main_align="center", z_index=1,
            children=[text_stack, hero_node]
        )
        
        container_group = GroupNode(
            id="main_container", name="Branded Container", x=spec.padding, y=spec.padding,
            width=float(spec.width - spec.padding * 2), height=float(spec.height - spec.padding * 2),
            layout_mode="absolute", z_index=1, children=[card_bg, content_stack]
        )
        return Layout(canvas=canvas, scene_tree=[container_group], metadata=Metadata(created_by="CompositionEngine", template=spec.name, version="1.0"))
