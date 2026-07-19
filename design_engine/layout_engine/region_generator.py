from pydantic import BaseModel

class SemanticRegionRatio(BaseModel):
    name: str
    width_ratio: float
    height_ratio: float

class RegionGenerator:
    @staticmethod
    def allocate_regions(layout, strategy: str) -> dict[str, SemanticRegionRatio]:
        """
        Pass 3: Allocates semantic layout region ratio limits (no pixel values).
        """
        regions = {
            "HeroRegion": SemanticRegionRatio(name="HeroRegion", width_ratio=0.85, height_ratio=0.45),
            "HeadlineRegion": SemanticRegionRatio(name="HeadlineRegion", width_ratio=0.90, height_ratio=0.18),
            "DescriptionRegion": SemanticRegionRatio(name="DescriptionRegion", width_ratio=0.90, height_ratio=0.12),
            "CTARegion": SemanticRegionRatio(name="CTARegion", width_ratio=0.60, height_ratio=0.08),
            "LogoRegion": SemanticRegionRatio(name="LogoRegion", width_ratio=0.30, height_ratio=0.10)
        }
        
        object.__setattr__(layout, "semantic_regions", regions)
        return regions
