from fastapi import HTTPException, status
from .models import User


class PostNotExistException(Exception):
    def __init__(self, post_id: int):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} does not exist")


class UserNotExistException(Exception):
    def __init__(self, user_id: int):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {user_id} does not exist")
