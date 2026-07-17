from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator
from design_engine.scene_graph.node import Node, validate_hex_color

class Canvas(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    background_color: str = Field(default="#FFFFFF")
    unit: Literal["px", "in", "cm"] = Field(default="px")

    @field_validator("background_color")
    @classmethod
    def check_background_color(cls, v: str) -> str:
        return validate_hex_color(v)

class Metadata(BaseModel):
    created_by: str = Field(default="Creative Canvas AI")
    template: Optional[str] = Field(default=None)
    version: str = Field(default="1.0")

class Layout(BaseModel):
    canvas: Canvas
    scene_tree: list[Node] = Field(..., description="Root nodes of the design scene graph")
    metadata: Metadata
