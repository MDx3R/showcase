"""Common domain exceptions."""


class DomainError(Exception):
    """Base class for all domain exceptions."""

    pass


class InvariantViolationError(DomainError):
    """Raised when a domain invariant is violated."""

    pass


class EntityNotFoundError(DomainError):
    """Raised when an entity cannot be found."""

    pass
