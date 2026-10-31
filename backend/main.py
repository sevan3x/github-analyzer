from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from github_api import get_user_data, get_user_repos
from github_user import User


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/user")
def get_user(username: str):
    """
    TODO:
    add logic here adn return meaningful response
    """
    return {"message": "Not implemented"}