from pydantic import BaseModel, Field
from typing import List, Optional

class SemanticNode(BaseModel):
    id: str = Field(..., description="Unique element ID")
    section: str = Field(..., description="Semantic section: background, logo, hero, description, cta, footer")
    role: str = Field(..., description="Semantic role: headline, description, logo_image, hero_image, button, footer_text")
    priority: str = Field(default="medium", description="Priority level: high, medium, low")
    style: str = Field(default="default", description="Styling accent: primary, secondary, outline")
    content: Optional[str] = Field(default=None, description="Inner text copy or image asset URL")

class SemanticScene(BaseModel):
    elements: List[SemanticNode] = Field(default_factory=list)
