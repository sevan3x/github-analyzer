class GitHubUser:
    def __init__(self, username):
        self.username = username
        self.followers = None
        self.repos = []

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