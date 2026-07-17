from typing import Optional
from pydantic import BaseModel, Field, field_validator
from design_engine.scene_graph.node import validate_hex_color, ShadowEffect, GradientProperties

class BrandKit(BaseModel):
    name: str = Field(..., description="Brand or business name")
    primary_color: str = Field(default="#0F172A", description="Primary theme color")
    secondary_color: str = Field(default="#1E293B", description="Secondary container color")
    accent_color: str = Field(default="#38BDF8", description="Accent draw color")
    font_heading: str = Field(default="Arial")
    font_body: str = Field(default="Arial")
    border_radius_default: int = Field(default=16, ge=0)
    logo_url: Optional[str] = Field(default=None)

    # Design Tokens Presets
    shadow_preset: Optional[ShadowEffect] = Field(
        default=ShadowEffect(type="drop_shadow", color="#000000", offset_x=0.0, offset_y=12.0, blur=24.0)
    )
    gradient_preset: Optional[GradientProperties] = Field(
        default=GradientProperties(colors=["#38BDF8", "#0EA5E9"], angle=90.0)
    )
    spacing_scale: float = Field(default=1.0, ge=0.0)
    button_radius: int = Field(default=24, ge=0)

    @field_validator("primary_color", "secondary_color", "accent_color")
    @classmethod
    def check_colors(cls, v: str) -> str:
        return validate_hex_color(v)
