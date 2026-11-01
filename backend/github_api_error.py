class GitHubAPIError(Exception):
    def __init__(
        self, message, code, status_code=None, retry_after=None, rate_limit_reset=None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.retry_after = retry_after
        self.rate_limit_reset = rate_limit_reset
