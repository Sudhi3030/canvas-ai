from typing import Dict
from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import ShadowEffect, GradientProperties
from design_engine.brand.brand_kit import BrandKit
from design_engine.template_slots.models import TemplateSlotRegistry
from design_engine.layout_planner.planner import LayoutPlanner
from design_engine.semantic_scene.models import SemanticScene

class VariantGenerator:
    def __init__(self, planner: LayoutPlanner = None):
        self.planner = planner or LayoutPlanner()

    def generate_variants(self, scene: SemanticScene, template_name: str, brand: BrandKit) -> Dict[str, Layout]:
        """
        Generates 5 distinct design theme variants from the target semantic scene.
        """
        spec = TemplateSlotRegistry.get_template_spec(template_name)
        
        # Define styling profiles for the 5 themes
        profiles = {
            "Minimal": {
                "font_heading": "Arial",
                "font_body": "Arial",
                "bg_color": "#F8FAFC",
                "card_color": "#FFFFFF",
                "accent_color": "#0F172A",
                "border_radius": 8,
                "spacing_scale": 1.2,
                "shadow_preset": None,
                "gradient_preset": None,
                "button_radius": 4
            },
            "Modern": {
                "font_heading": "Arial",
                "font_body": "Arial",
                "bg_color": "#0F172A",
                "card_color": "#1E293B",
                "accent_color": "#38BDF8",
                "border_radius": 24,
                "spacing_scale": 1.0,
                "shadow_preset": ShadowEffect(type="drop_shadow", color="#000000", offset_x=0.0, offset_y=12.0, blur=24.0),
                "gradient_preset": GradientProperties(colors=["#38BDF8", "#0EA5E9"], angle=90.0),
                "button_radius": 24
            },
            "Premium": {
                "font_heading": "Georgia",
                "font_body": "Georgia",
                "bg_color": "#111827",
                "card_color": "#1F2937",
                "accent_color": "#D97706",
                "border_radius": 16,
                "spacing_scale": 1.1,
                "shadow_preset": ShadowEffect(type="drop_shadow", color="#000000", offset_x=0.0, offset_y=16.0, blur=32.0),
                "gradient_preset": None,
                "button_radius": 12
            },
            "Bold": {
                "font_heading": "Trebuchet MS",
                "font_body": "Trebuchet MS",
                "bg_color": "#F59E0B",
                "card_color": "#10B981",
                "accent_color": "#FFFFFF",
                "border_radius": 0,
                "spacing_scale": 0.8,
                "shadow_preset": None,
                "gradient_preset": None,
                "button_radius": 0
            },
            "Luxury": {
                "font_heading": "Times New Roman",
                "font_body": "Times New Roman",
                "bg_color": "#050505",
                "card_color": "#000000",
                "accent_color": "#F59E0B", # Muted gold accent
                "border_radius": 32,
                "spacing_scale": 1.4,
                "shadow_preset": ShadowEffect(type="drop_shadow", color="#000000", offset_x=0.0, offset_y=8.0, blur=16.0),
                "gradient_preset": None,
                "button_radius": 32
            }
        }
        
        variants = {}
        for theme, style in profiles.items():
            variants[theme] = self.planner.plan_layout(scene, spec, brand, style)
            
        return variants
