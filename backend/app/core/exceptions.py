"""
app/core/exceptions.py
Domain-specific exception hierarchy.  Each exception carries an error `code`
(from constants) so API error handlers can serialize it consistently.
"""

from app.core.constants import AuthErrorCode, AlertErrorCode, GenericErrorCode


class AppException(Exception):
    """Base for all application exceptions."""

    def __init__(self, *, code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


class UnauthorizedException(AppException):
    def __init__(
        self,
        *,
        code: str = AuthErrorCode.TOKEN_INVALID,
        message: str = "Authentication required.",
    ) -> None:
        super().__init__(code=code, message=message, status_code=401)


class ForbiddenException(AppException):
    def __init__(
        self,
        *,
        code: str = AuthErrorCode.INSUFFICIENT_PERMISSIONS,
        message: str = "You do not have permission to perform this action.",
    ) -> None:
        super().__init__(code=code, message=message, status_code=403)


class NotFoundException(AppException):
    def __init__(
        self,
        *,
        code: str = GenericErrorCode.NOT_FOUND,
        message: str = "The requested resource was not found.",
    ) -> None:
        super().__init__(code=code, message=message, status_code=404)


class ConflictException(AppException):
    def __init__(self, *, code: str, message: str) -> None:
        super().__init__(code=code, message=message, status_code=409)


class AccountLockedException(AppException):
    def __init__(self, message: str = "Account is temporarily locked.") -> None:
        super().__init__(
            code=AuthErrorCode.ACCOUNT_LOCKED, message=message, status_code=423
        )


class DuplicateAlertException(ConflictException):
    def __init__(self) -> None:
        super().__init__(
            code=AlertErrorCode.DUPLICATE_ALERT,
            message="A similar alert is already active for this location.",
        )


class ServiceUnavailableException(AppException):
    def __init__(self, message: str = "Service temporarily unavailable.") -> None:
        super().__init__(
            code=AlertErrorCode.SERVICE_UNAVAILABLE, message=message, status_code=503
        )
