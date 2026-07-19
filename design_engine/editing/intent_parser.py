from design_engine.editing.models import ParsedIntent
from design_engine.editing.exceptions import InvalidCommandException

class IntentParser:
    def parse(self, prompt: str) -> ParsedIntent:
        """
        Parses natural language edit commands into structured edit intents.
        """
        prompt_lower = prompt.lower()
        
        # 1. Resize Commands
        if "bigger" in prompt_lower or "larger" in prompt_lower or "increase size" in prompt_lower:
            target = "title" if "title" in prompt_lower else ("button" if "button" in prompt_lower or "cta" in prompt_lower else "all")
            return ParsedIntent(action="resize", target=target, properties={"font_size_scale": 1.3, "width_scale": 1.3, "height_scale": 1.3})
            
        if "smaller" in prompt_lower or "reduce text size" in prompt_lower or "reduce size" in prompt_lower:
            target = "title" if "title" in prompt_lower else ("body" if "body" in prompt_lower else "all")
            return ParsedIntent(action="resize", target=target, properties={"font_size_scale": 0.8, "width_scale": 0.8, "height_scale": 0.8})
            
        # 2. Movement Commands
        if "move" in prompt_lower or "position" in prompt_lower:
            target = "logo" if "logo" in prompt_lower else "all"
            if "top left" in prompt_lower:
                return ParsedIntent(action="move", target=target, properties={"x": 15.0, "y": 15.0})
            elif "center" in prompt_lower:
                return ParsedIntent(action="move", target=target, properties={"align": "center"})
                
        if "center" in prompt_lower and ("cta" in prompt_lower or "button" in prompt_lower):
            return ParsedIntent(action="move", target="cta", properties={"align": "center"})
            
        # 3. Styling Commands
        if "round" in prompt_lower or "corners" in prompt_lower:
            return ParsedIntent(action="style_shift", target="all", properties={"border_radius": 15.0})
            
        if "premium" in prompt_lower or "modern" in prompt_lower:
            return ParsedIntent(action="style_shift", target="all", properties={"style": "premium" if "premium" in prompt_lower else "modern"})
            
        # 4. Color Commands
        if "blue" in prompt_lower:
            return ParsedIntent(action="recolor", target="background", properties={"color": "#1D4ED8"})
        if "darker" in prompt_lower or "dark" in prompt_lower:
            return ParsedIntent(action="recolor", target="background", properties={"color": "#0F172A"})
        if "background" in prompt_lower:
            return ParsedIntent(action="recolor", target="background", properties={"color": "#1E293B"})
            
        raise InvalidCommandException(f"Could not parse edit intent prompt: '{prompt}'")
