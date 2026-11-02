import requests
from github_api_error import GitHubAPIError


class GithubClient:
    def __init__(self, timeout=10, headers=None):
        self.timeout = timeout
        self.headers = headers

    def request_github(self, url, params=None):
        # Handle connection issues
        try:
            response = requests.get(
                url, params=params, headers=self.headers, timeout=self.timeout
            )
        except requests.Timeout as error:
            raise GitHubAPIError(
                "GitHub took too long to respond. Please try again.", "timeout"
            ) from error
        except requests.ConnectionError as error:
            raise GitHubAPIError(
                "Could not connect to GitHub. Please try again.", "connection_error"
            ) from error
        except requests.RequestException as error:
            raise GitHubAPIError(
                "The request to GitHub failed. Please try again.", "request_error"
            ) from error

        status = response.status_code
        if status == 404:
            raise GitHubAPIError(
                "GitHub user was not found.", "user_not_found", status_code=status
            )

        # Handle invalid json response
        try:
            data = response.json()
        except ValueError as error:
            if status == 200:
                raise GitHubAPIError(
                    "GitHub returned invalid JSON.", "invalid_response", status_code=status
                ) from error
            # Error responses may contain HTML or no body at all.
            data = None

        if status == 200:
            return response, data

        # Handle rate limit exceeding
        if self._is_rate_limited(response, data):
            raise GitHubAPIError(
                "GitHub API rate limit exceeded. Please try again later.",
                "rate_limit",
                status_code=status,
                retry_after=response.headers.get("Retry-After"),
                rate_limit_reset=response.headers.get("X-RateLimit-Reset"),
            )

        # Handle Github API http errors
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            if status == 401:
                message = "GitHub rejected the request's authentication."
            elif status == 403:
                message = "GitHub denied access to the requested data."
            elif status >= 500:
                message = "GitHub is temporarily unavailable. Please try again later."
            else:
                message = f"GitHub request failed with HTTP status {status}."
            raise GitHubAPIError(
                message, "http_error", status_code=status
            ) from error

        # Handle any unexpected error
        raise GitHubAPIError(
            "GitHub returned an unexpected response.", "invalid_response", status_code=status
        )

    def _is_rate_limited(self, response, data):
        if response.status_code == 429:
            return True
        if response.status_code != 403:
            return False

        if response.headers.get("X-RateLimit-Remaining") == "0" or "Retry-After" in response.headers:
            return True

        if not isinstance(data, dict):
            return False

        message = data.get("message", "")
        return isinstance(message, str) and "rate limit" in message.lower()
