class AssetException(Exception):
    """Base exception for all asset management issues."""
    pass

class AssetNotFoundException(AssetException):
    """Raised when an asset does not exist in local disk or remote provider."""
    pass

class InvalidAssetFormatException(AssetException):
    """Raised when an asset file contains invalid headers or is corrupted."""
    pass

class DownloadTimeoutException(AssetException):
    """Raised when downloading a remote asset times out."""
    pass

class AccessDeniedException(AssetException):
    """Raised when a resource has forbidden access limits."""
    pass
