from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from github_api import get_user_data, get_user_repos
from github_user import GitHubUser
from github_api_error import GitHubAPIError


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/user")
def get_user(
    username: str = Query(
        ...,
        min_length=1,
        max_length=39,
        pattern=r"^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$",
        description=(
            "GitHub username: contains letters or numbers, optionally separated by single dash."
        ),
    ),
):
    try:
        profile = get_user_data(username)
        repos = get_user_repos(username)
    except GitHubAPIError as error:
        if error.code == "user_not_found":
            status_code = 404
        elif error.code == "rate_limit":
            status_code = 429
        elif error.code == "timeout":
            status_code = 504
        else:
            status_code = 502
            
        raise HTTPException(status_code=status_code, detail=error.message) from error

    user = GitHubUser(profile["login"], profile["followers"], repos)

    return user.to_dict()