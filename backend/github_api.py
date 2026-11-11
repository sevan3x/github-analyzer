from typing import Any, Dict, List

from github_client import GithubClient
from github_api_error import GitHubAPIError
from github_types import GitHubRepository


GH_CLIENT = GithubClient()


def get_user_data(username: str) -> Dict[str, Any]:
    """Return profile data, raising GitHubAPIError if fetching it fails."""
    data = GH_CLIENT.get_json(f"/users/{username}")

    if not isinstance(data, dict):
        raise GitHubAPIError(
            "GitHub returned invalid user data.",
            "invalid_response",
        )
    return data


def get_user_repos(username: str) -> List[GitHubRepository]:
    """Return public repositories, raising GitHubAPIError on fetching failures."""
    repos: List[GitHubRepository] = []
    data = GH_CLIENT.get_all_pages(f"/users/{username}/repos")

    for fetched_repo in data:
        if not isinstance(fetched_repo, dict) or "name" not in fetched_repo:
            raise GitHubAPIError(
                "GitHub returned invalid repository data.",
                "invalid_response",
            )

        repos.append({"name": fetched_repo["name"], "language": fetched_repo.get("language")})

    return repos
