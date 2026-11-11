from typing import Any, Dict, List, Optional, Set

from github_types import GitHubRepository


class GitHubUser:
    def __init__(
        self,
        username: str,
        followers: Optional[int] = None,
        repos: Optional[List[GitHubRepository]] = None,
    ) -> None:
        self.username: str = username
        self.followers: Optional[int] = followers
        self.repos: List[GitHubRepository] = [] if repos is None else repos

    def get_most_used_language(self) -> Optional[str]:
        language_counts: Dict[str, int] = {}

        for repo in self.repos:
            if repo['language'] is None:
                continue

            if repo['language'] in language_counts:
                language_counts[repo['language']] += 1
            else:
                language_counts[repo['language']] = 1

        most_used_lang: Optional[str] = None
        highest_count = 0

        for lang, count in language_counts.items():
            if count > highest_count:
                most_used_lang = lang
                highest_count = count

        # when two languages are with the same count, it returns the one encountered first
        # the approach here should be decided
        return most_used_lang

    def get_all_languages(self) -> List[str]:
        languages: Set[str] = set()

        for repo in self.repos:
            lang = repo["language"]
            if lang is not None:
                languages.add(lang)

        return sorted(languages)

    def to_dict(self) -> Dict[str, Any]:
        messages: List[str] = []

        if self.followers == 0:
            messages.append("This user has no followers.")

        if not self.repos:
            messages.append("This user has no repositories.")

        return {
            "username": self.username,
            "followers": self.followers,
            "repos": self.repos,
            "most_used_language": self.get_most_used_language(),
            "languages": self.get_all_languages(),
            "messages": messages,
        }
