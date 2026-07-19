from pydantic import BaseModel, Field
from typing import List, Optional

class StylingConfig(BaseModel):
    theme: str
    font_heading: str
    font_body: str
    bg_gradient_colors: List[str] = Field(default_factory=list)
    card_opacity: float = 0.9
    border_radius: float = 12.0
    spacing_scale: float = 1.0
