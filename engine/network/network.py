
from typing import Any, Dict
import aiohttp
from ..exceptions import (
    EngineError,
    InvalidAPIKeyError,
    APILimitExceededError,
    NetworkError,
    UnexpectedResponseError,
)


class Network:
    """
    Handles asynchronous HTTP GET requests with comprehensive error handling.

    Attributes:
        base_url (str): The base URL for all requests.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def request(
            self, params: Dict[str, Any], timeout: int = 10) -> Dict[str, Any]:
        """
        Perform an asynchronous HTTP GET request with query parameters.

        Args:
            params (Dict[str, Any]): Query parameters for the request.
            timeout (int, optional): Timeout for the request in seconds. Defaults to 10.

        Returns:
            Dict[str, Any]: Parsed JSON response from the server.

        Raises:
            InvalidAPIKeyError: Raised when the API key is invalid or unauthorized.
            APILimitExceededError: Raised when API rate limit is exceeded.
            UnexpectedResponseError: Raised for unexpected HTTP status codes without detailed error messages.
            NetworkError: Raised on network-related issues.
            EngineError: Raised for other unhandled exceptions.
        """
        timeout_obj = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout_obj) as session:
            try:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        data = await response.json(content_type=None)
                        if "error" in data:
                            error_message = data["error"].get("message", "")
                            if "key" in error_message.lower():
                                raise InvalidAPIKeyError(error_message)
                            if "quota" in error_message.lower():
                                raise APILimitExceededError(error_message)
                            raise EngineError(error_message)
                        raise UnexpectedResponseError(
                            f"Unexpected HTTP status: {response.status}")
                    return await response.json(content_type=None)
            except (InvalidAPIKeyError, APILimitExceededError, NetworkError):
                raise
            except aiohttp.ClientConnectionError as error:
                raise NetworkError(
                    f"Network connection error: {error}") from error
            except Exception as error:
                raise EngineError(
                    f"Unhandled network error: {error}") from error
