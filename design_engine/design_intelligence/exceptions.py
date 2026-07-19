class DesignIntelligenceException(Exception):
    """Base exception for all design intelligence evaluation errors."""
    pass

class RuleViolationException(DesignIntelligenceException):
    """Raised when a design rule threshold is violated."""
    pass
