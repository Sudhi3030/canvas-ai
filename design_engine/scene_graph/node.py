from typing import Annotated, Literal, Optional, Union, List, ForwardRef
from pydantic import BaseModel, Field, field_validator, model_validator
import re

HEX_COLOR_REGEX = re.compile(r"^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})$")

def validate_hex_color(v: str) -> str:
    if not HEX_COLOR_REGEX.match(v):
        raise ValueError("Invalid hex color format.")
    return v.upper()

# Element Specific Properties
class TextProperties(BaseModel):
    content: str = Field(..., min_length=1)
    font_family: str = Field(default="Arial")
    font_size: float = Field(gt=0)
    font_weight: str = Field(default="normal")
    color: str = Field(default="#000000")
    
    # Advanced Typography Parameters
    line_height: float = Field(default=1.2, gt=0.0)
    letter_spacing: float = Field(default=0.0, ge=0.0)
    align: Literal["left", "center", "right"] = Field(default="left")
    vertical_align: Literal["top", "middle", "bottom"] = Field(default="top")
    
    # Strokes & Drop Shadows
    stroke_color: Optional[str] = Field(default=None)
    stroke_width: int = Field(default=0, ge=0)
    shadow_color: Optional[str] = Field(default=None)
    shadow_offset_x: float = Field(default=0.0)
    shadow_offset_y: float = Field(default=0.0)

    @field_validator("color", "stroke_color", "shadow_color")
    @classmethod
    def check_colors(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_hex_color(v)

class ImageProperties(BaseModel):
    url: Optional[str] = Field(default=None)
    alt_text: Optional[str] = Field(default=None)
    
    # Fit mode options
    fit_mode: Literal["cover", "contain", "fill"] = Field(default="fill")
    
    # Corner Clip Masks
    border_radius: int = Field(default=0, ge=0)
    clip_circle: bool = Field(default=False)
    
    # Image Filters
    blur: float = Field(default=0.0, ge=0.0)
    brightness: float = Field(default=1.0, ge=0.0)
    contrast: float = Field(default=1.0, ge=0.0)
    saturation: float = Field(default=1.0, ge=0.0)

class GradientProperties(BaseModel):
    colors: List[str] = Field(..., min_length=2)
    angle: float = Field(default=0.0)

    @field_validator("colors")
    @classmethod
    def check_gradient_colors(cls, v: List[str]) -> List[str]:
        return [validate_hex_color(c) for c in v]

class ShapeProperties(BaseModel):
    fill_color: str = Field(default="#CCCCCC")
    stroke_color: Optional[str] = Field(default=None)
    stroke_width: int = Field(default=0, ge=0)
    border_radius: int = Field(default=0, ge=0)
    
    # Gradient properties
    fill_gradient: Optional[GradientProperties] = None
    
    # Shadow styling
    shadow_color: Optional[str] = Field(default=None)
    shadow_offset_x: float = Field(default=0.0)
    shadow_offset_y: float = Field(default=0.0)
    shadow_blur: float = Field(default=0.0, ge=0.0)

    @field_validator("fill_color", "stroke_color", "shadow_color")
    @classmethod
    def check_colors(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_hex_color(v)

# Sizing policy models
SizingPolicy = Literal["fixed", "fill", "fit"]

class AnimationProperties(BaseModel):
    effect: Literal["fade", "slide_in", "scale_in", "rotate_in"] = Field(default="fade")
    duration: float = Field(default=1.0, ge=0.0)
    delay: float = Field(default=0.0, ge=0.0)

class ShadowEffect(BaseModel):
    type: Literal["drop_shadow", "inner_shadow"] = "drop_shadow"
    color: str = Field(default="#000000")
    offset_x: float = Field(default=0.0)
    offset_y: float = Field(default=0.0)
    blur: float = Field(default=4.0, ge=0.0)

    @field_validator("color")
    @classmethod
    def check_color(cls, v: str) -> str:
        return validate_hex_color(v)

class GlowEffect(BaseModel):
    type: Literal["glow"] = "glow"
    color: str = Field(default="#FFFFFF")
    blur: float = Field(default=8.0, ge=0.0)

    @field_validator("color")
    @classmethod
    def check_color(cls, v: str) -> str:
        return validate_hex_color(v)

class BlurEffect(BaseModel):
    type: Literal["blur"] = "blur"
    radius: float = Field(default=4.0, ge=0.0)

Effect = Annotated[
    Union[ShadowEffect, GlowEffect, BlurEffect],
    Field(discriminator="type")
]

# Base Scene Graph Node containing geometry/state
class BaseNode(BaseModel):
    id: str = Field(..., description="Unique node identifier")
    name: str = Field(..., description="Human readable layer name")
    
    # Coordinates (used when parent is absolute layout)
    x: float = Field(default=0.0)
    y: float = Field(default=0.0)
    
    # Dimensions (used as base size when policy is fixed)
    width: float = Field(default=100.0, gt=0)
    height: float = Field(default=100.0, gt=0)
    
    # Sizing policies for auto-layout engines
    width_policy: SizingPolicy = Field(default="fixed")
    height_policy: SizingPolicy = Field(default="fixed")
    
    rotation: float = Field(default=0.0)
    z_index: int = Field(default=1, ge=0)
    opacity: float = Field(default=1.0, ge=0.0, le=1.0)
    visible: bool = Field(default=True)
    locked: bool = Field(default=False)
    
    # Reusable post-processing effects
    effects: List[Effect] = Field(default_factory=list)
    
    # Animation properties metadata
    animation: Optional[AnimationProperties] = Field(default=None)

# Specific elements subclasses
class TextNode(BaseNode):
    type: Literal["text"] = "text"
    properties: TextProperties

class ImageNode(BaseNode):
    type: Literal["image"] = "image"
    properties: ImageProperties

class ShapeNode(BaseNode):
    type: Literal["shape"] = "shape"
    properties: ShapeProperties

# Recursive Node forward reference declaration
NodeRef = ForwardRef('Node')

class GroupNode(BaseNode):
    type: Literal["group"] = "group"
    
    # Flow Layout Properties
    layout_mode: Literal["absolute", "horizontal", "vertical"] = Field(default="absolute")
    spacing: float = Field(default=0.0)
    padding_left: float = Field(default=0.0)
    padding_right: float = Field(default=0.0)
    padding_top: float = Field(default=0.0)
    padding_bottom: float = Field(default=0.0)
    
    cross_align: Literal["start", "center", "end", "stretch"] = Field(default="start")
    main_align: Literal["start", "center", "end", "space-between"] = Field(default="start")
    
    children: List['NodeRef'] = Field(default_factory=list)

class ComponentNode(GroupNode):
    type: Literal["component"] = "component"
    component_type: Literal["button"] = "button"
    
    # Custom properties for component templates
    label: str = Field(default="Click Me")
    bg_color: str = Field(default="#38BDF8")
    text_color: str = Field(default="#0F172A")
    border_radius: int = Field(default=8)
    
    icon_url: Optional[str] = None
    icon_width: float = Field(default=20.0)
    icon_height: float = Field(default=20.0)
    
    state: Literal["default", "hover", "pressed"] = Field(default="default")

    @model_validator(mode="after")
    def compile_component(self) -> 'ComponentNode':
        if not self.children and self.component_type == "button":
            # 1. Background capsule shape
            bg_node = ShapeNode(
                id=f"{self.id}_bg",
                name=f"{self.name} Background",
                x=0, y=0,
                width_policy="fill",
                height_policy="fill",
                z_index=1,
                properties={
                    "fill_color": self.bg_color,
                    "border_radius": self.border_radius
                }
            )
            
            # 2. Text label
            text_node = TextNode(
                id=f"{self.id}_label",
                name=f"{self.name} Label",
                width_policy="fit",
                height_policy="fit",
                z_index=2,
                properties={
                    "content": self.label,
                    "font_family": "Arial",
                    "font_size": 16.0,
                    "color": self.text_color,
                    "font_weight": "bold",
                    "align": "center",
                    "vertical_align": "middle"
                }
            )
            
            # 3. Stack container
            stack_children = []
            if self.icon_url:
                icon_node = ImageNode(
                    id=f"{self.id}_icon",
                    name=f"{self.name} Icon",
                    width=self.icon_width,
                    height=self.icon_height,
                    width_policy="fixed",
                    height_policy="fixed",
                    z_index=2,
                    properties={
                        "url": self.icon_url,
                        "fit_mode": "contain"
                    }
                )
                stack_children.append(icon_node)
                
            stack_children.append(text_node)
            
            # Align label and optional icon horizontally in the center
            aligner = GroupNode(
                id=f"{self.id}_aligner",
                name=f"{self.name} Aligner",
                x=0, y=0,
                width_policy="fill",
                height_policy="fill",
                layout_mode="horizontal",
                spacing=8.0,
                cross_align="center",
                main_align="center",
                z_index=2,
                children=stack_children
            )
            
            # Group layout mode
            self.layout_mode = "absolute"
            self.children = [bg_node, aligner]
            
        return self

# Union of all node types annotated with a discriminator
Node = Annotated[
    Union[TextNode, ImageNode, ShapeNode, GroupNode, ComponentNode],
    Field(discriminator="type")
]

# Rebuild GroupNode and ComponentNode to link recursive references
GroupNode.model_rebuild()
ComponentNode.model_rebuild()
