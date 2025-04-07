from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.auth import get_current_user
from core.database import SessionLocal
from models.post_model import Post
from models.user_model import User
from schemas.post_schema import PostCreate, PostOut
from services.post_service import add_post, get_user_posts, delete_post
from functools import lru_cache

# Initialize API router for post-related routes
router = APIRouter()


def get_db():
    """
    Dependency function that provides a scoped SQLAlchemy session.
    Ensures the session is properly closed after the request ends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache(maxsize=128)
def get_cached_posts(db: Session):
    """
    Example of a cached database query using LRU cache.
    Not used actively in routes, but can be used to reduce DB hits.

    :param db: SQLAlchemy session
    :return: List of all posts from the database
    """
    posts = db.query(Post).all()
    return posts


@router.post("/add")
def create_post(
        post_data: PostCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """
    Endpoint to create a new post.

    :param post_data: Data required to create a post
    :param current_user: User creating the post (from JWT token)
    :param db: SQLAlchemy session
    :return: ID of the newly created post
    """
    post_id = add_post(current_user, post_data, db)
    return {"post_id": post_id}


@router.get("/get", response_model=list[PostOut])
def read_posts(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """
    Endpoint to retrieve all posts belonging to the authenticated user.

    :param current_user: The current logged-in user
    :param db: SQLAlchemy session
    :return: List of user's posts
    """
    return get_user_posts(current_user, db)


@router.delete("/delete/{post_id}")
def remove_post(
        post_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """
    Endpoint to delete a post by its ID, if it belongs to the current user.

    :param post_id: ID of the post to delete
    :param current_user: The current logged-in user
    :param db: SQLAlchemy session
    :return: Success confirmation message
    """
    delete_post(current_user, post_id, db)
    return {"detail": "Post deleted"}
