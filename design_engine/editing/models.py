from pydantic import BaseModel, Field
from typing import Dict, Any, Literal

class ParsedIntent(BaseModel):
    action: Literal["resize", "move", "style_shift", "replace_content", "recolor"]
    target: str
    properties: Dict[str, Any] = Field(default_factory=dict)
