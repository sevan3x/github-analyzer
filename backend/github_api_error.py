from enum import Enum
from typing import Optional


class GitHubErrorCode(str, Enum):
    RESOURCE_NOT_FOUND = "resource_not_found"
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    CONNECTION_ERROR = "connection_error"
    REQUEST_ERROR = "request_error"
    HTTP_ERROR = "http_error"
    INVALID_RESPONSE = "invalid_response"


class GitHubAPIError(Exception):
    def __init__(
        self,
        message: str,
        code: GitHubErrorCode,
        status_code: Optional[int] = None,
        retry_after: Optional[str] = None,
        rate_limit_reset: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code: GitHubErrorCode = code
        self.status_code = status_code
        self.retry_after = retry_after
        self.rate_limit_reset = rate_limit_reset
