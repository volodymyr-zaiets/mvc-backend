from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from core.database import Base


class Post(Base):
    """
    SQLAlchemy model representing a post entity in the database.

    Each post is associated with a specific user and contains textual content
    along with a timestamp indicating when it was created.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    # Foreign key linking this post to a user; cascade deletes on user deletion
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Main content of the post
    text = Column(Text, nullable=False)
    # Timestamp automatically set to current time when the post is created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Defines a relationship to the User model; allows access to the post's author
    user = relationship("User", backref="posts")
