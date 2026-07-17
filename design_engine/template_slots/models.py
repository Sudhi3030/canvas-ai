from design_engine.brand.templates import TemplateSlot, TemplateSpec, TEMPLATES

class TemplateSlotRegistry:
    @staticmethod
    def get_template_spec(name: str) -> TemplateSpec:
        """
        Retrieves the template spec by name, falling back to Instagram.
        """
        return TEMPLATES.get(name, TEMPLATES["Instagram"])
