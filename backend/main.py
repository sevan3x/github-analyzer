from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from github_api import get_user_data, get_user_repos
from github_user import GitHubUser


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
            "GitHub username: letters or numbers, optionally separated by single dash."
        ),
    ),
):
    """
    TODO:
    add logic here adn return meaningful response
    """
    return {"message": "Not implemented"}
