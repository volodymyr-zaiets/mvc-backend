from pydantic import BaseModel, constr
from datetime import datetime


class PostCreate(BaseModel):
    """
    Pydantic schema for creating a new post.

    This schema validates the data when a user submits a new post.
    It ensures that the post's text is not empty and does not exceed the maximum size.
    """
    # Post text: must be between 1 and 1 MB in size.
    text: constr(min_length=1, max_length=1024*1024)  # Validates that the text has a minimum length of 1 and max length of 1 MB.


class PostOut(BaseModel):
    """
    Pydantic schema for returning a post's data after creation or retrieval.

    This schema is used to serialize the post object when sending data back to the client.
    """
    id: int  # The unique identifier for the post
    text: str  # The content of the post
    created_at: datetime  # Timestamp when the post was created

    class Config:
        # This option allows the model to accept data from ORM objects like SQLAlchemy models
        from_attributes = True
