class WhitespaceEngine:
    @staticmethod
    def get_layout_whitespace(canvas_height: float) -> dict[str, float]:
        """
        Dynamically computes spacing and margins scale steps.
        """
        margin = max(30.0, canvas_height * 0.05)
        gap = max(15.0, canvas_height * 0.025)
        return {
            "outer_margin": margin,
            "section_gap": gap,
            "padding": margin
        }
