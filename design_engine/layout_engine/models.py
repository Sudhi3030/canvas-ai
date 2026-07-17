from pydantic import BaseModel, Field
from typing import Optional

class MarginPadding(BaseModel):
    left: float = Field(default=0.0, ge=0.0)
    right: float = Field(default=0.0, ge=0.0)
    top: float = Field(default=0.0, ge=0.0)
    bottom: float = Field(default=0.0, ge=0.0)

class ConstraintSpec(BaseModel):
    min_width: Optional[float] = None
    max_width: Optional[float] = None
    min_height: Optional[float] = None
    max_height: Optional[float] = None
    aspect_ratio: Optional[float] = None
