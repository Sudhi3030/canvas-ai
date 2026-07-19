class EditingException(Exception):
    """Base exception for editing actions errors."""
    pass

class InvalidCommandException(EditingException):
    """Raised when an edit command cannot be parsed or matched."""
    pass
