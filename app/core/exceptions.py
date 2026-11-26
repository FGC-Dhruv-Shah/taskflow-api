"""Domain-level exceptions shared across services and repositories."""


class TaskFlowError(Exception):
    """Base class for all application-defined errors."""


class ValidationError(TaskFlowError):
    """Raised when user-supplied input fails a validation rule."""


class NotFoundError(TaskFlowError):
    """Raised when a requested entity does not exist."""


class PermissionDeniedError(TaskFlowError):
    """Raised when the acting user is not allowed to perform an operation."""


class ConflictError(TaskFlowError):
    """Raised when an operation would violate a uniqueness or state constraint."""
