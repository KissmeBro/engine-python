class EngineError(Exception):
    """Base exception for engine-related errors."""
    pass


class InvalidAPIKeyError(EngineError):
    """Exception raised for invalid or unauthorized API keys."""

    def __init__(self, message: str = "API key is invalid or unauthorized."):
        super().__init__(message)


class APILimitExceededError(EngineError):
    """Exception raised when API rate limits are exceeded."""

    def __init__(
            self,
            message: str = "API quota exceeded. Please wait until quota resets or upgrade your plan."):
        super().__init__(message)


class NetworkError(EngineError):
    """Exception raised for network-related errors."""

    def __init__(self, message: str = "Network connection error occurred."):
        super().__init__(message)


class UnexpectedResponseError(EngineError):
    """Exception raised for unexpected HTTP responses."""

    def __init__(self, message: str = "Unexpected HTTP response received."):
        super().__init__(message)
