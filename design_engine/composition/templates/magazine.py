from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import GroupNode, ShapeNode, TextNode, ImageNode, ComponentNode, ShapeProperties
from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateSpec

class MagazineTemplate:
    @staticmethod
    def build(spec: TemplateSpec, brand: BrandKit, logo: str, heading: str, body: str, cta: str, hero_url: str) -> Layout:
        canvas = Canvas(width=spec.width, height=spec.height, background_color="#FFFFFF")
        
        # Hero Image covers top 60% height
        hero_h = float(spec.height) * 0.60
        hero_node = ImageNode(id="hero", name="Magazine Hero Image", x=0, y=0, width=float(spec.width), height=hero_h, z_index=0, properties={"url": hero_url, "fit_mode": "cover"})
        
        # Bottom card panel
        panel_y = hero_h - 40.0
        panel_h = float(spec.height) - panel_y
        card_bg = ShapeNode(id="card_bg", name="Bottom Card Panel", x=0, y=panel_y, width=float(spec.width), height=panel_h, z_index=1, properties=ShapeProperties(border_radius=16.0))
        
        logo_node = ImageNode(id="logo", name="Logo", width=80.0, height=80.0, width_policy="fixed", height_policy="fixed", z_index=2, properties={"url": logo, "fit_mode": "contain"})
        headline_node = TextNode(id="heading", name="Headline", width_policy="fill", height_policy="fit", z_index=2, properties={"content": heading, "font_family": "Georgia", "font_size": 36.0, "color": "#000000", "align": "center"})
        body_node = TextNode(id="body", name="Description", width_policy="fill", height_policy="fit", z_index=3, properties={"content": body, "font_family": "Arial", "font_size": 18.0, "color": "#475569", "align": "center"})
        cta_node = ComponentNode(id="cta", name="CTA Button", width=220.0, height=55.0, width_policy="fixed", height_policy="fixed", z_index=4, label=cta)
        
        bottom_stack = GroupNode(
            id="bottom_stack", name="Text Stack", x=0, y=panel_y, width_policy="fill", height=panel_h,
            layout_mode="vertical", spacing=15.0, padding_left=30.0, padding_right=30.0, padding_top=20.0, padding_bottom=20.0,
            cross_align="center", main_align="center", z_index=2,
            children=[logo_node, headline_node, body_node, cta_node]
        )
        
        container_group = GroupNode(
            id="main_container", name="Branded Container", x=0, y=0,
            width=float(spec.width), height=float(spec.height),
            layout_mode="absolute", z_index=1, children=[hero_node, card_bg, bottom_stack]
        )
        return Layout(canvas=canvas, scene_tree=[container_group], metadata=Metadata(created_by="CompositionEngine", template=spec.name, version="1.0"))
