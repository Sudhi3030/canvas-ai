from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import GroupNode, ShapeNode, TextNode, ImageNode, ComponentNode, ShapeProperties
from design_engine.brand.brand_kit import BrandKit
from design_engine.brand.templates import TemplateSpec

class OverlayTemplate:
    @staticmethod
    def build(spec: TemplateSpec, brand: BrandKit, logo: str, heading: str, body: str, cta: str, hero_url: str) -> Layout:
        canvas = Canvas(width=spec.width, height=spec.height, background_color="#FFFFFF")
        
        # Hero Image spans the entire canvas as background
        hero_bg = ImageNode(id="hero", name="Background Hero Image", x=0, y=0, width_policy="fill", height_policy="fill", z_index=0, properties={"url": hero_url, "fit_mode": "cover"})
        
        # Semi-transparent dark overlay panel
        overlay_mask = ShapeNode(id="overlay_mask", name="Overlay Mask", x=0, y=0, width_policy="fill", height_policy="fill", z_index=1, properties={"fill_color": "#000000", "stroke_color": None, "stroke_width": 0.0}, opacity=0.5)
        
        logo_node = ImageNode(id="logo", name="Logo", width=80.0, height=80.0, width_policy="fixed", height_policy="fixed", z_index=2, properties={"url": logo, "fit_mode": "contain"})
        headline_node = TextNode(id="heading", name="Headline", width_policy="fill", height_policy="fit", z_index=3, properties={"content": heading, "font_family": "Arial", "font_size": 48.0, "color": "#FFFFFF", "align": "center"})
        body_node = TextNode(id="body", name="Description", width_policy="fill", height_policy="fit", z_index=4, properties={"content": body, "font_family": "Arial", "font_size": 22.0, "color": "#E2E8F0", "align": "center"})
        cta_node = ComponentNode(id="cta", name="CTA Button", width=240.0, height=60.0, width_policy="fixed", height_policy="fixed", z_index=5, label=cta)
        
        content_stack = GroupNode(
            id="content_stack", name="Content Stack", x=0, y=0, width_policy="fill", height_policy="fill",
            layout_mode="vertical", spacing=25.0, padding_left=40.0, padding_right=40.0, padding_top=50.0, padding_bottom=50.0,
            cross_align="center", main_align="center", z_index=2,
            children=[logo_node, headline_node, body_node, cta_node]
        )
        
        container_group = GroupNode(
            id="main_container", name="Branded Container", x=spec.padding, y=spec.padding,
            width=float(spec.width - spec.padding * 2), height=float(spec.height - spec.padding * 2),
            layout_mode="absolute", z_index=1, children=[hero_bg, overlay_mask, content_stack]
        )
        return Layout(canvas=canvas, scene_tree=[container_group], metadata=Metadata(created_by="CompositionEngine", template=spec.name, version="1.0"))
