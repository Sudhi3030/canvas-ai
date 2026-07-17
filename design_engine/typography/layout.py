import os
from typing import Dict, List, Optional, Tuple, Any

class TypographyEngine:
    @staticmethod
    def layout_text(
        content: str,
        font_family: str,
        font_size: float,
        width: float,
        height: float,
        line_height: float,
        letter_spacing: float,
        align: str,
        vertical_align: str,
        asset_manager: Any,
        word_spacing: float = 0.0,
        paragraph_spacing: float = 0.0
    ) -> Dict[str, Any]:
        """
        Solves line wrapping and computes relative x, y coordinates for each text line
        inside the node container dimensions. Automatically scales down font size
        to prevent overflow if the height is bounded.
        """
        current_font_size = font_size
        min_font_size = 10.0
        
        lines = []
        final_font = None
        total_height = 0.0
        line_height_px = 0.0
        
        # 1. Run Auto-Fit font scaling check if height is bounded
        while current_font_size >= min_font_size:
            final_font = asset_manager.load_font(font_family, current_font_size)
            lines = TypographyEngine._wrap_lines(
                content, final_font, width, letter_spacing, word_spacing
            )
            
            # Retrieve line vertical bounding metrics
            bbox = final_font.getbbox("Ap")
            line_height_px = (bbox[3] - bbox[1]) * line_height
            
            total_height = len(lines) * line_height_px + (len(lines) - 1) * paragraph_spacing
            
            if height <= 0 or total_height <= height:
                break
            
            current_font_size -= 1.0 # decrement font size to scale fit

        # 2. Compute Vertical Alignment offsets
        start_y = 0.0
        if height > 0 and total_height < height:
            if vertical_align == "middle":
                start_y = (height - total_height) / 2.0
            elif vertical_align == "bottom":
                start_y = height - total_height

        # 3. Compute Horizontal Alignment offsets and build Solved Lines
        resolved_lines = []
        current_y = start_y
        
        for idx, line_text in enumerate(lines):
            # Calculate width of this line
            line_w = final_font.getlength(line_text)
            # Add spacings
            line_w += letter_spacing * (len(line_text) - 1)
            words = line_text.split(" ")
            line_w += word_spacing * (len(words) - 1)
            
            # Align horizontally
            start_x = 0.0
            if width > 0 and line_w < width:
                if align == "center":
                    start_x = (width - line_w) / 2.0
                elif align == "right":
                    start_x = width - line_w
            
            resolved_lines.append({
                "text": line_text,
                "x": start_x,
                "y": current_y,
                "width": line_w,
                "height": line_height_px
            })
            
            current_y += line_height_px + paragraph_spacing

        return {
            "lines": resolved_lines,
            "font_size": current_font_size
        }

    @staticmethod
    def _wrap_lines(
        content: str, font, max_width: float, letter_spacing: float, word_spacing: float
    ) -> List[str]:
        if max_width <= 0:
            return [content]

        def measure_string(s: str) -> float:
            if not s:
                return 0.0
            length = font.getlength(s)
            length += letter_spacing * (len(s) - 1)
            words_count = len(s.split(" "))
            length += word_spacing * (words_count - 1)
            return length

        paragraphs = content.split("\n")
        lines = []

        for para in paragraphs:
            words = para.split(" ")
            current_line = []
            
            for word in words:
                test_line = " ".join(current_line + [word]) if current_line else word
                if measure_string(test_line) <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        # Single word is wider than max_width: force split character by character
                        char_accum = ""
                        for char in word:
                            test_char_line = char_accum + char
                            if measure_string(test_char_line) <= max_width:
                                char_accum = test_char_line
                            else:
                                if char_accum:
                                    lines.append(char_accum)
                                char_accum = char
                        if char_accum:
                            current_line = [char_accum]
            if current_line:
                lines.append(" ".join(current_line))
                
        return lines
