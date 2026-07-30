"""
Custom exceptions for API clients.
"""


class APIError(Exception):
    """Base exception for all API-related errors."""


class AuthenticationError(APIError):
    """Authentication failed."""


class AuthorizationError(APIError):
    """Permission denied."""


class NotFoundError(APIError):
    """Requested resource was not found."""


class RateLimitError(APIError):
    """API rate limit exceeded."""


class ServerError(APIError):
    """Server-side error."""


class InvalidJSONError(APIError):
    """Response does not contain valid JSON."""


class UnexpectedContentTypeError(APIError):
    """Unexpected response content type."""


class ValidationError(APIError):
    """Response validation failed."""
