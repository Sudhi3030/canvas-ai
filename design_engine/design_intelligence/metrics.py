from design_engine.scene_graph.document import Layout

class DesignMetrics:
    @staticmethod
    def compile_metrics(layout: Layout, score: float) -> None:
        """
        Calculates and records design metrics details inside layout metadata fields.
        """
        if layout.metadata is not None:
            layout.metadata.template = f"aesthetic_score:{score:.1f}"
