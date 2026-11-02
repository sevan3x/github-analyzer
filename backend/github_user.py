class GitHubUser:
    def __init__(self, username, followers=None, repos=None):
        self.username = username
        self.followers = followers
        self.repos = [] if repos is None else repos

    def get_most_used_language(self):
        language_counts = {}

        for repo in self.repos:
            if repo['language'] is None:
                continue

            if repo['language'] in language_counts:
                language_counts[repo['language']] += 1
            else:
                language_counts[repo['language']] = 1

        most_used_lang = None
        highest_count = 0

        for lang, count in language_counts.items():
            if count > highest_count:
                most_used_lang = lang
                highest_count = count

        # when two languages are with the same count, it returns the one encountered first
        # the approach here should be decided
        return most_used_lang

    def get_all_languages(self):
        languages = set()

        for repo in self.repos:
            lang = repo["language"]
            if lang is not None:
                languages.add(lang)

        return sorted(languages)

    def to_dict(self):
        messages = []

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