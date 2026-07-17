import os
from PIL import Image
from typing import Tuple

class ThumbnailEngine:
    def __init__(self, cache_dir: str = "outputs/thumbnails"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def generate_thumbnail(self, image: Image.Image, asset_id: str, size: Tuple[int, int] = (150, 150)) -> str:
        """
        Creates and stores scaled thumbnail images to avoid redundant regenerations.
        """
        out_path = os.path.join(self.cache_dir, f"{asset_id}_thumb.png")
        if os.path.exists(out_path):
            return out_path
        try:
            thumb = image.copy()
            thumb.thumbnail(size, Image.Resampling.LANCZOS)
            thumb.save(out_path, "PNG")
            return out_path
        except Exception:
            return ""
