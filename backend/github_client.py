from typing import Any, Dict, List, Mapping, Optional, Tuple
from urllib.parse import urljoin

import requests
from github_api_error import GitHubAPIError, GitHubErrorCode


class GithubClient:
    def __init__(
        self,
        timeout: float = 10,
        headers: Optional[Dict[str, str]] = None,
        base_url: str = "https://api.github.com",
    ) -> None:
        self.timeout: float = timeout
        self.headers: Optional[Dict[str, str]] = headers
        self.base_url: str = base_url.rstrip("/") + "/"

    def get_json(
        self, path: str, params: Optional[Mapping[str, Any]] = None
    ) -> Any:
        """Return parsed JSON without exposing the HTTP response."""
        _, data = self._request_github(path, params=params)
        return data

    def get_all_pages(
        self, path: str, params: Optional[Mapping[str, Any]] = None
    ) -> List[Any]:
        """Collect a paginated list, raising an error if any page fails."""
        items: List[Any] = []
        url: Optional[str] = path
        query: Optional[Dict[str, Any]] = dict(params) if params is not None else {}
        query.setdefault("per_page", 100)

        while url:
            response, data = self._request_github(url, params=query)
            if not isinstance(data, list):
                raise GitHubAPIError(
                    "GitHub returned invalid paginated data.",
                    GitHubErrorCode.INVALID_RESPONSE,
                    status_code=response.status_code,
                )

            items.extend(data)
            url = response.links.get("next", {}).get("url")
            # GitHub's next-page URL already includes its query parameters.
            query = None

        return items

    def _request_github(
        self, path: str, params: Optional[Mapping[str, Any]] = None
    ) -> Tuple[requests.Response, Any]:
        response = self._send_request(path, params)
        data = self._parse_json(response)
        self._check_status(response, data)
        return response, data

    def _send_request(
        self, path: str, params: Optional[Mapping[str, Any]] = None
    ) -> requests.Response:
        """Send a request and translate connection failures."""
        url = urljoin(self.base_url, path.lstrip("/"))
        try:
            return requests.get(
                url, params=params, headers=self.headers, timeout=self.timeout
            )
        except requests.Timeout as error:
            raise GitHubAPIError(
                "GitHub took too long to respond. Please try again.",
                GitHubErrorCode.TIMEOUT,
            ) from error
        except requests.ConnectionError as error:
            raise GitHubAPIError(
                "Could not connect to GitHub. Please try again.",
                GitHubErrorCode.CONNECTION_ERROR,
            ) from error
        except requests.RequestException as error:
            raise GitHubAPIError(
                "The request to GitHub failed. Please try again.",
                GitHubErrorCode.REQUEST_ERROR,
            ) from error

    def _parse_json(self, response: requests.Response) -> Any:
        """Parse JSON, allowing non-JSON bodies on unsuccessful responses."""
        try:
            return response.json()
        except ValueError as error:
            # Error responses may contain HTML or no body at all.
            if response.status_code != 200:
                return None

            raise GitHubAPIError(
                "GitHub returned invalid JSON.",
                GitHubErrorCode.INVALID_RESPONSE,
                status_code=response.status_code,
            ) from error

    def _check_status(self, response: requests.Response, data: object) -> None:
        """Check success, missing resources, rate limits, and other statuses."""
        status = response.status_code
        if status == 200:
            return

        if status == 404:
            raise GitHubAPIError(
                "GitHub resource was not found.",
                GitHubErrorCode.RESOURCE_NOT_FOUND,
                status_code=status,
            )

        if self._is_rate_limited(response, data):
            raise GitHubAPIError(
                "GitHub API rate limit exceeded. Please try again later.",
                GitHubErrorCode.RATE_LIMIT,
                status_code=status,
                retry_after=response.headers.get("Retry-After"),
                rate_limit_reset=response.headers.get("X-RateLimit-Reset"),
            )

        self._raise_for_http_error(response)
        raise GitHubAPIError(
            "GitHub returned an unexpected response.",
            GitHubErrorCode.INVALID_RESPONSE,
            status_code=status,
        )

    def _raise_for_http_error(self, response: requests.Response) -> None:
        """Translate HTTP errors while preserving their original cause."""
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            status = response.status_code
            if status == 401:
                message = "GitHub rejected the request's authentication."
            elif status == 403:
                message = "GitHub denied access to the requested data."
            elif status >= 500:
                message = "GitHub is temporarily unavailable. Please try again later."
            else:
                message = f"GitHub request failed with HTTP status {status}."
            raise GitHubAPIError(
                message, GitHubErrorCode.HTTP_ERROR, status_code=status
            ) from error

    def _is_rate_limited(self, response: requests.Response, data: object) -> bool:
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
