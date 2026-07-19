class AlignmentEngine:
    @staticmethod
    def get_text_align(composition_style: str) -> str:
        """
        Maps composition styles to text alignment choices.
        """
        if composition_style in ("editorial", "minimal"):
            return "left"
        return "center"
