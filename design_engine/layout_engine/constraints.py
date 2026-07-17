from typing import Optional

class ConstraintSolver:
    @staticmethod
    def clamp_width(width: float, min_w: Optional[float], max_w: Optional[float]) -> float:
        if min_w is not None:
            width = max(width, min_w)
        if max_w is not None:
            width = min(width, max_w)
        return width

    @staticmethod
    def clamp_height(height: float, min_h: Optional[float], max_h: Optional[float]) -> float:
        if min_h is not None:
            height = max(height, min_h)
        if max_h is not None:
            height = min(height, max_h)
        return height

    @staticmethod
    def apply_aspect_ratio(
        width: float,
        height: float,
        aspect_ratio: Optional[float],
        width_policy: str,
        height_policy: str
    ) -> tuple[float, float]:
        if aspect_ratio is not None and aspect_ratio > 0:
            if width_policy == "fixed" and height_policy == "fit":
                height = width / aspect_ratio
            elif height_policy == "fixed" and width_policy == "fit":
                width = height * aspect_ratio
        return width, height
