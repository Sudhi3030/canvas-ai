import hashlib
from typing import Dict, Optional
from design_engine.assets.metadata import AssetMetadata

class AssetRegistry:
    def __init__(self):
        self.metadata_store: Dict[str, AssetMetadata] = {}
        # maps md5 -> asset_id of the first registered instance
        self.hash_store: Dict[str, str] = {}

    def compute_hash(self, content_bytes: bytes) -> str:
        """
        Computes MD5 hash checksum of asset bytes.
        """
        return hashlib.md5(content_bytes).hexdigest()

    def get_asset_by_hash(self, checksum: str) -> Optional[str]:
        return self.hash_store.get(checksum)

    def register(self, metadata: AssetMetadata) -> None:
        self.metadata_store[metadata.asset_id] = metadata
        if metadata.checksum:
            self.hash_store[metadata.checksum] = metadata.asset_id

    def get(self, asset_id: str) -> Optional[AssetMetadata]:
        return self.metadata_store.get(asset_id)

    def remove(self, asset_id: str) -> None:
        meta = self.metadata_store.pop(asset_id, None)
        if meta and meta.checksum:
            self.hash_store.pop(meta.checksum, None)
