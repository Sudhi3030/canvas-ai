class AlignmentEngine:
    @staticmethod
    def align_horizontal(
        avail_width: float,
        content_width: float,
        align_mode: str,
        padding_left: float
    ) -> float:
        """Computes left offset based on horizontal alignment policy."""
        offset = padding_left
        if align_mode == "center":
            offset += (avail_width - content_width) / 2.0
        elif align_mode == "end":
            offset += avail_width - content_width
        return offset

    @staticmethod
    def align_vertical(
        avail_height: float,
        content_height: float,
        align_mode: str,
        padding_top: float
    ) -> float:
        """Computes top offset based on vertical alignment policy."""
        offset = padding_top
        if align_mode == "center" or align_mode == "middle":
            offset += (avail_height - content_height) / 2.0
        elif align_mode == "end":
            offset += avail_height - content_height
        return offset
