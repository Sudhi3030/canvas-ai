from PIL import Image
from io import BytesIO
from design_engine.assets.exceptions import InvalidAssetFormatException

class AssetOptimizer:
    @staticmethod
    def optimize_image(image_bytes: bytes) -> Image.Image:
        """
        Normalizes and optimizes image files for rendering.
        """
        try:
            img = Image.open(BytesIO(image_bytes))
            # Resolve EXIF rotation orientation mapping if available
            try:
                from PIL import ImageOps
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass
            return img.convert("RGBA")
        except Exception as e:
            raise InvalidAssetFormatException(f"Corrupted or invalid image format: {e}")
