"""
Custom exceptions for the Metal Trend Analysis project.
"""


class MetalTrendException(Exception):
    """Base exception class for the Metal Trend Analysis project."""
    pass


class ConfigurationError(MetalTrendException):
    """Raised when there's an issue with configuration."""
    pass


class DataFetchError(MetalTrendException):
    """Raised when data fetching fails."""
    pass


class AnalysisError(MetalTrendException):
    """Raised when analysis operations fail."""
    pass


class NotificationError(MetalTrendException):
    """Raised when notification sending fails."""
    pass


class ValidationError(MetalTrendException):
    """Raised when data validation fails."""
    pass


class LLMError(MetalTrendException):
    """Raised when LLM operations fail."""
    pass


class RetryableError(MetalTrendException):
    """Base class for errors that can be retried."""
    pass


class NetworkError(RetryableError):
    """Raised when network operations fail."""
    pass


class TimeoutError(RetryableError):
    """Raised when operations timeout."""
    pass