from design_engine.layout_engine.layout import LayoutSolver

def wrap_text(content: str, font, max_width: float, letter_spacing: float = 0.0) -> list[str]:
    """Backward compatible wrapper delegating to TypographyEngine."""
    from design_engine.typography.layout import TypographyEngine
    return TypographyEngine._wrap_lines(content, font, max_width, letter_spacing, 0.0)
