"""Post database model."""

import enum
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class PostStatus(enum.Enum):
    """Post status enumeration.
    
    Attributes:
        PUBLIC: Post is visible to everyone.
        UNPUBLIC: Post is hidden from public.
        DRAFT: Post is still being edited.
        DELETED: Post is marked as deleted (soft delete).
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    UNPUBLISHED = "unpublished"
    DELETED = "deleted"

class Post(Base):
    """Post model for database storage.

    Attributes:
        id: Unique identifier for the post.
        title: Title of the post (1-200 characters).
        content: Content of the post.
        user_id: Identifier of the user who authored the post.
        created_at: Timestamp when the post was created.
        updated_at: Timestamp when the post was last updated.
    """

    __tablename__ = "posts"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Post information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus),
        default=PostStatus.DRAFT,
        nullable=False
    )

    # Foreign key to User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        """String representation of Post.

        Returns:
            String representation showing title, status, and user_id.
        """
        return f"<Post(title='{self.title}', status={self.status}, user_id={self.user_id})>"
