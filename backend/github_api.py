from github_client import GithubClient
from github_api_error import GitHubAPIError


BASE_URL = "https://api.github.com"
REQUEST_TIMEOUT = 10
HEADERS = {"Accept": "application/vnd.github+json"}

GH_CLIENT = GithubClient(REQUEST_TIMEOUT, HEADERS)


def get_user_data(username):
    """
    call the GitHub API and return a dict with data or None (actually now raising GitHubAPIError)
    """
    response, data = GH_CLIENT.request_github(f"{BASE_URL}/users/{username}")

    if not isinstance(data, dict):
        raise GitHubAPIError(
            "GitHub returned invalid user data.",
            "invalid_response",
            status_code=response.status_code,
        )
    return data


def get_user_repos(username):
    """
    call the GitHub API and return a list of dicts(repos name, language/technology) 
    with data or None (actually now raising GitHubAPIError)
    """
    repos = []
    url = f"{BASE_URL}/users/{username}/repos"
    params = {"per_page": 100}

    while url:
        response, data = GH_CLIENT.request_github(url, params=params)

        if not isinstance(data, list):
            raise GitHubAPIError(
                "GitHub returned invalid repository data.",
                "invalid_response",
                status_code=response.status_code,
            )

        for fetched_repo in data:
            if not isinstance(fetched_repo, dict) or "name" not in fetched_repo:
                raise GitHubAPIError(
                    "GitHub returned invalid repository data.",
                    "invalid_response",
                    status_code=response.status_code,
                )

            repos.append({"name": fetched_repo["name"], "language": fetched_repo.get("language")})
        url = response.links.get("next", {}).get("url")

        # Pagination URLs already contain their query params, 
        # so we don't need to pass them.
        # ex: https://api.github.com/users/random_user/repos?per_page=100&page=2
        params = None

    return repos
