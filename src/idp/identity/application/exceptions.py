from uuid import UUID

from common.application.exceptions import ApplicationError, NotFoundError


class IdentityNotFoundError(NotFoundError):
    pass


class EmailAlreadyTakenError(ApplicationError):
    def __init__(self, email: str):
        super().__init__(f"Email '{email}' is already taken by another user.")
        self.email = email


class InvalidPasswordError(ApplicationError):
    def __init__(self, identity_id: UUID) -> None:
        super().__init__(f"Invalid password for user {identity_id}")
        self.identity_id = identity_id


class InvalidEmailError(ApplicationError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Invalid email: {email}")
        self.email = email


class TokenExpiredError(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Token expired")


class TokenRevokedError(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Token revoked")


class InvalidTokenError(ApplicationError):
    def __init__(self, message: str = "Invalid token") -> None:
        super().__init__(message)
