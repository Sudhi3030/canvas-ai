from pydantic import BaseModel

class FontPair(BaseModel):
    heading: str
    body: str
    letter_spacing: float = 0.0
    line_height: float = 1.25

class TypographyPairingEngine:
    PAIRS = {
        "luxury": FontPair(heading="Georgia", body="Times New Roman", letter_spacing=2.0, line_height=1.2),
        "modern": FontPair(heading="Arial", body="Arial", letter_spacing=1.0, line_height=1.3),
        "minimal": FontPair(heading="Arial", body="Arial", letter_spacing=0.5, line_height=1.4),
        "bold": FontPair(heading="Trebuchet MS", body="Trebuchet MS", letter_spacing=2.5, line_height=1.15),
        "elegant": FontPair(heading="Times New Roman", body="Times New Roman", letter_spacing=1.5, line_height=1.25)
    }

    @classmethod
    def get_pairing(cls, style: str) -> FontPair:
        return cls.PAIRS.get(style.lower(), cls.PAIRS["modern"])
