from enum import Enum

class CompositionType(str, Enum):
    HERO = "hero"
    SPLIT = "split"
    OVERLAY = "overlay"
    MAGAZINE = "magazine"
    EDITORIAL = "editorial"
    POSTER = "poster"
    BENTO = "bento"
    MINIMAL = "minimal"
    STORY = "story"
    CARD = "card"
