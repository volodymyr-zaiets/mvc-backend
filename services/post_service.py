from sqlalchemy.orm import Session
from models.post_model import Post
from schemas.post_schema import PostCreate
from models.user_model import User
from fastapi import HTTPException
from core.cache import cache


def add_post(user: User, post_data: PostCreate, db: Session) -> int:
    """
    Adds a new post for a user.

    This function performs the following actions:
    1. Creates a new Post object using the provided post data.
    2. Adds the new post to the database and commits the transaction.
    3. Refreshes the post object to ensure it has the most up-to-date data.
    4. Invalidates the user's cache to ensure the cache is refreshed for subsequent post queries.
    5. Returns the ID of the newly created post.

    Args:
        user (User): The user who is creating the post.
        post_data (PostCreate): The data for the new post (text).
        db (Session): The SQLAlchemy session object used to interact with the database.

    Returns:
        int: The ID of the newly created post.

    Raises:
        None
    """
    # Create a new post object
    post = Post(user_id=user.id, text=post_data.text)

    # Add the post to the database and commit the changes
    db.add(post)
    db.commit()
    db.refresh(post)  # Refresh the post object with data from the database

    # Invalidate the user's cache to refresh it
    cache.invalidate(user.id)

    # Return the ID of the created post
    return post.id


def get_user_posts(user: User, db: Session):
    """
    Retrieves the posts of a given user.

    This function first checks the cache for the user's posts:
    1. If cached posts are found, they are returned immediately.
    2. If no cached posts are found, the posts are queried from the database.
    3. After retrieving the posts, they are cached for future use.

    Args:
        user (User): The user whose posts need to be fetched.
        db (Session): The SQLAlchemy session object used to interact with the database.

    Returns:
        list: A list of the user's posts.

    Raises:
        None
    """
    # Try to get posts from the cache
    cached = cache.get(user.id)
    if cached is not None:
        return cached

    # If not cached, fetch the posts from the database
    posts = db.query(Post).filter(Post.user_id == user.id).order_by(Post.created_at.desc()).all()

    # Cache the retrieved posts for future use
    cache.set(user.id, posts)

    # Return the list of posts
    return posts


def delete_post(user: User, post_id: int, db: Session):
    """
    Deletes a post by the given post ID.

    This function performs the following steps:
    1. Checks if the post exists and if it belongs to the specified user.
    2. If the post is found, it is deleted from the database.
    3. The database transaction is committed.
    4. Invalidates the user's cache to refresh the data for future requests.

    Args:
        user (User): The user attempting to delete the post.
        post_id (int): The ID of the post to be deleted.
        db (Session): The SQLAlchemy session object used to interact with the database.

    Returns:
        None

    Raises:
        HTTPException: If the post is not found or does not belong to the user (status code 404).
    """
    # Find the post by ID and ensure it belongs to the current user
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
    if not post:
        # If post not found, raise HTTP exception with 404 status
        raise HTTPException(status_code=404, detail="Post not found")

    # Delete the post from the database
    db.delete(post)
    db.commit()

    # Invalidate the user's cache to ensure it is updated
    cache.invalidate(user.id)
