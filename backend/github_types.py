from typing import Optional, TypedDict


class GitHubRepository(TypedDict):
    name: str
    language: Optional[str]
