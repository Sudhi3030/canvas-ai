from pydantic import BaseModel
from typing import Dict

class DesignSystemColors(BaseModel):
    primary: str
    secondary: str
    accent: str
    neutral: str
    highlight: str
    cta: str
    surface: str
    shadow: str
    overlay: str
    border: str

class ColorHarmonyEngine:
    PALETTES: Dict[str, DesignSystemColors] = {
        "luxury": DesignSystemColors(
            primary="#111827", secondary="#4B5563", accent="#D97706",
            neutral="#F9FAFB", highlight="#FBBF24", cta="#D97706",
            surface="#1F2937", shadow="#000000", overlay="#2E2528", border="#D97706"
        ),
        "modern": DesignSystemColors(
            primary="#1E1B4B", secondary="#4338CA", accent="#F43F5E",
            neutral="#F8FAFC", highlight="#FB7185", cta="#F43F5E",
            surface="#FFFFFF", shadow="#000000", overlay="#111827", border="#E2E8F0"
        ),
        "minimal": DesignSystemColors(
            primary="#18181B", secondary="#71717A", accent="#27272A",
            neutral="#FAFAFA", highlight="#27272A", cta="#18181B",
            surface="#FFFFFF", shadow="#000000", overlay="#000000", border="#E4E4E7"
        ),
        "bold": DesignSystemColors(
            primary="#FFFFFF", secondary="#E2E8F0", accent="#F59E0B",
            neutral="#1E293B", highlight="#EF4444", cta="#F59E0B",
            surface="#0F172A", shadow="#000000", overlay="#000000", border="#F59E0B"
        ),
        "elegant": DesignSystemColors(
            primary="#2E2528", secondary="#705C63", accent="#BE95C4",
            neutral="#FFF8FA", highlight="#D4A373", cta="#BE95C4",
            surface="#F3E9DC", shadow="#000000", overlay="#2E2528", border="#E3D5CA"
        )
    }

    @classmethod
    def get_colors(cls, style: str) -> DesignSystemColors:
        return cls.PALETTES.get(style.lower(), cls.PALETTES["modern"])
