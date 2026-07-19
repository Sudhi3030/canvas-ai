from pydantic import BaseModel, Field
from typing import List

class ColorPalette(BaseModel):
    name: str
    primary: str
    secondary: str
    accent: str
    background: str

class DesignTokens(BaseModel):
    palettes: List[ColorPalette] = Field(default_factory=lambda: [
        ColorPalette(name="Premium", primary="#0F172A", secondary="#475569", accent="#D97706", background="#F8FAFC"),
        ColorPalette(name="Modern", primary="#1E1B4B", secondary="#4338CA", accent="#F43F5E", background="#FAF5FF"),
        ColorPalette(name="Minimal", primary="#18181B", secondary="#71717A", accent="#27272A", background="#FFFFFF"),
        ColorPalette(name="Bold", primary="#FFFFFF", secondary="#E2E8F0", accent="#F59E0B", background="#1E293B")
    ])
