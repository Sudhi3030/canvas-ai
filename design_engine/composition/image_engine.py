class ImagePlacementEngine:
    @staticmethod
    def get_proportional_hero_dimensions(canvas_w: float, canvas_h: float, occupancy_ratio: float = 0.45) -> tuple[float, float]:
        """
        Determines width & height for hero images covering the targeted canvas height occupancy ratio.
        """
        return float(canvas_w), float(canvas_h * occupancy_ratio)
