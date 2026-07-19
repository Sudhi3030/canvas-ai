from pydantic import BaseModel

class GridSpec(BaseModel):
    columns: int = 12
    margin: float = 40.0
    gutter: float = 20.0
    width: float = 800.0

class GridGenerator:
    @staticmethod
    def get_column_width(spec: GridSpec) -> float:
        """Calculates width of a single grid column."""
        total_gutter_w = spec.gutter * (spec.columns - 1)
        avail_w = spec.width - (spec.margin * 2) - total_gutter_w
        return max(10.0, avail_w / spec.columns)

    @staticmethod
    def get_span_width(spec: GridSpec, span: int) -> float:
        """Calculates width across a span of columns including gutters."""
        col_w = GridGenerator.get_column_width(spec)
        return (col_w * span) + (spec.gutter * (span - 1))
