from typing import Dict, Tuple

PLATFORM_SAFE_AREAS: Dict[str, Tuple[float, float, float, float]] = {
    # platform -> (left, right, top, bottom)
    "Instagram Feed": (50.0, 50.0, 50.0, 50.0),
    "Instagram Story": (80.0, 80.0, 150.0, 150.0),
    "Facebook Post": (40.0, 40.0, 40.0, 40.0),
    "Pinterest Pin": (30.0, 30.0, 50.0, 50.0),
    "Default": (20.0, 20.0, 20.0, 20.0)
}
