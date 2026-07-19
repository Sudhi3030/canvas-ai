class CompositionPlanner:
    @staticmethod
    def plan_composition(layout) -> str:
        """
        Pass 2: Selects composition strategy name.
        """
        strategy = "CENTERED_HERO"
        if hasattr(layout, "metadata") and layout.metadata is not None:
            if hasattr(layout.metadata, "template") and layout.metadata.template:
                strategy = layout.metadata.template.upper().replace(" ", "_")
        return strategy
