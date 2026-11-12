export interface GithubRepository {
    name: string;
    language: string | null;
}

export interface GithubUserResponse {
    username: string;
    followers: number;
    repos: GithubRepository[];
    most_used_language: string | null;
    languages: string[];
    messages: string[];
}