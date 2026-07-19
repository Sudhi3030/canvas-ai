class TypographyEngine:
    @staticmethod
    def get_proportional_sizes(canvas_width: float) -> dict[str, float]:
        """
        Determines font sizes proportional to canvas width.
        """
        if canvas_width >= 1000:
            return {
                "headline": 64.0,
                "subheading": 32.0,
                "description": 22.0,
                "cta": 24.0
            }
        else:
            return {
                "headline": 48.0,
                "subheading": 24.0,
                "description": 18.0,
                "cta": 18.0
            }
