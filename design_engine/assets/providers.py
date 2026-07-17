import os
import httpx
from abc import ABC, abstractmethod
from design_engine.assets.exceptions import AssetNotFoundException, DownloadTimeoutException, AccessDeniedException

class AssetProvider(ABC):
    @abstractmethod
    def read_bytes(self, source: str) -> bytes:
        """
        Loads the raw asset content as bytes.
        """
        pass

class LocalProvider(AssetProvider):
    def read_bytes(self, source: str) -> bytes:
        if not os.path.exists(source):
            raise AssetNotFoundException(f"Local asset not found: {source}")
        try:
            with open(source, "rb") as f:
                return f.read()
        except PermissionError:
            raise AccessDeniedException(f"Permission denied reading local asset: {source}")
        except Exception as e:
            raise AssetNotFoundException(f"Failed to read local asset: {e}")

class RemoteProvider(AssetProvider):
    def read_bytes(self, source: str) -> bytes:
        try:
            response = httpx.get(source, timeout=10.0)
            if response.status_code == 404:
                raise AssetNotFoundException(f"Remote asset returned 404: {source}")
            elif response.status_code == 403:
                raise AccessDeniedException(f"Access forbidden (403): {source}")
            response.raise_for_status()
            return response.content
        except httpx.TimeoutException:
            raise DownloadTimeoutException(f"Timeout downloading remote asset: {source}")
        except Exception as e:
            if isinstance(e, (AssetNotFoundException, AccessDeniedException)):
                raise e
            raise AssetNotFoundException(f"Failed to download remote asset: {e}")

class CloudProvider(AssetProvider):
    def read_bytes(self, source: str) -> bytes:
        raise NotImplementedError("CloudProvider integration is in progress.")
