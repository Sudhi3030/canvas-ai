import os
import uuid
from typing import Dict, Optional, Tuple, Any
from PIL import Image, ImageFont
from datetime import datetime, timezone

from design_engine.assets.types import AssetType
from design_engine.assets.metadata import AssetMetadata
from design_engine.assets.exceptions import AssetNotFoundException, InvalidAssetFormatException
from design_engine.assets.providers import LocalProvider, RemoteProvider
from design_engine.assets.cache import MemoryCache
from design_engine.assets.optimizer import AssetOptimizer
from design_engine.assets.thumbnail import ThumbnailEngine
from design_engine.assets.registry import AssetRegistry

class AssetManager:
    def __init__(self, cache_size: int = 256):
        self.local_provider = LocalProvider()
        self.remote_provider = RemoteProvider()
        
        self.image_cache = MemoryCache(maxsize=cache_size)
        self.font_cache = MemoryCache(maxsize=cache_size)
        self.registry = AssetRegistry()
        self.thumbnail_engine = ThumbnailEngine()
        
        # Maps source URL/path to asset_id
        self.source_to_id: Dict[str, str] = {}

    def load_asset(self, source: str, asset_type: AssetType) -> Any:
        if asset_type == AssetType.IMAGE:
            return self.load_image(source)
        elif asset_type == AssetType.FONT:
            # Assumes base size 16 if not specified
            return self.load_font(source, 16.0)
        elif asset_type == AssetType.SVG:
            return self.load_svg(source)
        else:
            raise NotImplementedError(f"Loader for {asset_type} is not implemented.")

    def load_image(self, source: str) -> Image.Image:
        """
        Loads, optimizes, caches, and returns a copy of an image asset.
        """
        asset_id = self.source_to_id.get(source)
        if asset_id:
            cached_img = self.image_cache.get(asset_id)
            if cached_img:
                return cached_img.copy()

        # Download or read raw bytes
        provider = self.remote_provider if source.startswith("http://") or source.startswith("https://") else self.local_provider
        raw_bytes = provider.read_bytes(source)
        
        # Duplicate detection by checksum hash
        md5_hash = self.registry.compute_hash(raw_bytes)
        dup_asset_id = self.registry.get_asset_by_hash(md5_hash)
        
        if dup_asset_id:
            self.source_to_id[source] = dup_asset_id
            cached_img = self.image_cache.get(dup_asset_id)
            if not cached_img:
                cached_img = AssetOptimizer.optimize_image(raw_bytes)
                self.image_cache.set(dup_asset_id, cached_img)
            return cached_img.copy()

        # If new asset: optimize, generate ID, and register
        optimized_img = AssetOptimizer.optimize_image(raw_bytes)
        new_id = f"asset_{uuid.uuid4().hex[:8]}"
        
        # Generate thumbnail path
        thumb_path = self.thumbnail_engine.generate_thumbnail(optimized_img, new_id)
        
        metadata = AssetMetadata(
            asset_id=new_id,
            name=os.path.basename(source),
            asset_type=AssetType.IMAGE,
            hash=md5_hash,
            mime_type="image/png",
            width=optimized_img.width,
            height=optimized_img.height,
            file_size=len(raw_bytes),
            source=source,
            cache_key=new_id,
            thumbnail_path=thumb_path,
            checksum=md5_hash
        )
        
        self.registry.register(metadata)
        self.source_to_id[source] = new_id
        self.image_cache.set(new_id, optimized_img)
        
        return optimized_img.copy()

    def load_font(self, font_family: str, size: float) -> ImageFont.ImageFont:
        """
        Loads TrueType font files from local or system directories using centralized caches.
        """
        cache_key = f"{font_family}_{int(size)}"
        cached_font = self.font_cache.get(cache_key)
        if cached_font:
            return cached_font

        # Find font path (backward compatible logic matching previous load_font)
        from design_engine.config import CONFIG
        FONTS_DIR = os.path.join(CONFIG.BASE_DIR, "assets", "fonts")
        font_filename = f"{font_family}.ttf"
        local_font_path = os.path.join(FONTS_DIR, font_filename)
        
        target_path = None
        if os.path.exists(local_font_path):
            target_path = local_font_path
        else:
            system_font_paths = [
                f"/Library/Fonts/{font_family}.ttf",
                f"/System/Library/Fonts/Supplemental/{font_family}.ttf",
                f"/System/Library/Fonts/{font_family}.ttf",
                f"/usr/share/fonts/truetype/dejavu/{font_family}.ttf",
                f"/usr/share/fonts/TTF/{font_family}.ttf",
                f"C:\\Windows\\Fonts\\{font_family}.ttf"
            ]
            for sys_path in system_font_paths:
                if os.path.exists(sys_path):
                    target_path = sys_path
                    break

        if not target_path:
            # Fallback to loading default PIL bitmap font
            font_obj = ImageFont.load_default()
        else:
            try:
                font_obj = ImageFont.truetype(target_path, int(size))
            except Exception as e:
                raise InvalidAssetFormatException(f"Corrupted or invalid font: {target_path} ({e})")

        self.font_cache.set(cache_key, font_obj)
        return font_obj

    def load_svg(self, source: str) -> str:
        """
        Load and return SVG text content.
        """
        provider = self.remote_provider if source.startswith("http://") or source.startswith("https://") else self.local_provider
        return provider.read_bytes(source).decode("utf-8", errors="ignore")

    def get_metadata(self, source: str) -> Optional[AssetMetadata]:
        asset_id = self.source_to_id.get(source)
        if asset_id:
            return self.registry.get(asset_id)
        return None

    def invalidate(self, source: str) -> None:
        """
        Invalidates memory cache entries matching the resource source and increments version counters.
        """
        asset_id = self.source_to_id.get(source)
        if asset_id:
            self.image_cache.remove(asset_id)
            meta = self.registry.get(asset_id)
            if meta:
                meta.version += 1
                meta.updated_at = datetime.now(timezone.utc)

    def clear_cache(self) -> None:
        self.image_cache.clear()
        self.font_cache.clear()

    def generate_thumbnail(self, source: str, size: Tuple[int, int] = (150, 150)) -> str:
        img = self.load_image(source)
        asset_id = self.source_to_id.get(source)
        if asset_id:
            return self.thumbnail_engine.generate_thumbnail(img, asset_id, size)
        return ""

    def register_asset(self, source: str, asset_type: AssetType) -> str:
        """
        Manually pre-registers an asset path inside the registry store.
        """
        if source in self.source_to_id:
            return self.source_to_id[source]
        new_id = f"asset_{uuid.uuid4().hex[:8]}"
        self.source_to_id[source] = new_id
        
        metadata = AssetMetadata(
            asset_id=new_id,
            name=os.path.basename(source),
            asset_type=asset_type,
            hash="",
            source=source,
            cache_key=new_id
        )
        self.registry.register(metadata)
        return new_id
