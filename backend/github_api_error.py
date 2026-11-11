from typing import Optional


class GitHubAPIError(Exception):
    def __init__(
        self,
        message: str,
        code: str,
        status_code: Optional[int] = None,
        retry_after: Optional[str] = None,
        rate_limit_reset: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.retry_after = retry_after
        self.rate_limit_reset = rate_limit_reset
