"""Pydantic schemas for Post API requests and responses."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class PostBase(BaseModel):
    """Base post schema with common fields.

    Attributes:
        title: Title of the post (1-200 characters).
        content: Content of the post.
        status: Status of the post (draft, published, unpublished, deleted).
    """

    title: str = Field(..., min_length=1, max_length=200, description="Title of the post")
    content: str = Field(..., description="Content of the post")
    status: str = Field(
        default="draft",
        pattern="^(draft|published|unpublished|deleted)$",
        description="Status of the post"
    )

class PostCreate(PostBase):
    """Schema for creating a new post.

    Inherits all fields from PostBase.
    """
    pass

class PostUpdate(BaseModel):
    """Schema for updating an existing post.

    All fields are optional to allow partial updates.

    Attributes:
        title: New title if updating.
        content: New content if updating.
        status: New status if updating.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    status: Optional[str] = Field(
        None,
        pattern="^(draft|published|unpublished|deleted)$"
    )

class PostResponse(PostBase):
    """Schema for post response.

    Attributes:
        id: Unique identifier for the post.
        user_id: Identifier of the user who authored the post.
        created_at: Timestamp when the post was created.
        updated_at: Timestamp when the post was last updated.
    """

    id: int = Field(..., description="Unique identifier for the post")
    user_id: int = Field(..., description="Identifier of the user who authored the post")
    created_at: datetime = Field(..., description="Timestamp when the post was created")
    updated_at: datetime = Field(..., description="Timestamp when the post was last updated")

    model_config = ConfigDict(from_attributes=True)

class PostListResponse(BaseModel):
    """Schema for paginated post list response.

    Attributes:
        total: Total number of posts.
        posts: List of PostResponse items.
    """

    posts: list[PostResponse] = Field(..., description="List of posts")
    total: int = Field(..., description="Total number of posts in database")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of posts per page")

    model_config = ConfigDict(from_attributes=True)

    