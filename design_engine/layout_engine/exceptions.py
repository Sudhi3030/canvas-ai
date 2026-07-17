class LayoutException(Exception):
    """Base exception for all layout errors."""
    pass

class InvalidConstraintException(LayoutException):
    """Raised when an invalid bounding or ratio constraint is specified."""
    pass

class LayoutOverflowException(LayoutException):
    """Raised when content dimensions exceed available bounding boxes."""
    pass
