from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from design_engine.assets.types import AssetType

class AssetMetadata(BaseModel):
    asset_id: str
    name: str
    asset_type: AssetType
    hash: str
    version: int = 1
    mime_type: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    file_size: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str
    cache_key: str
    thumbnail_path: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    author: Optional[str] = None
    license: Optional[str] = None
    checksum: Optional[str] = None
