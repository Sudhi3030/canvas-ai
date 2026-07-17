from enum import Enum

class AssetType(str, Enum):
    IMAGE = "IMAGE"
    FONT = "FONT"
    SVG = "SVG"
    ICON = "ICON"
    LOGO = "LOGO"
    TEXTURE = "TEXTURE"
    PATTERN = "PATTERN"
    GRADIENT = "GRADIENT"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
