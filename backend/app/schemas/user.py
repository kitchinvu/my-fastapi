"""Pydantic schemas for User API requests and responses."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common fields.

    Attributes:
        username: Unique username (3-50 characters).
        email: Valid email address.
        full_name: Optional full name (max 100 characters).
        role: User role (admin or user).
        is_active: Account activation status.
    """

    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="Valid email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    role: str = Field(default="user", pattern="^(admin|user)$", description="User role")
    is_active: bool = Field(default=True, description="Account active status")


class UserCreate(UserBase):
    """Schema for creating a new user.

    Attributes:
        password: Plain text password (min 8 characters) - will be hashed before storage.
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (min 8 characters)"
    )


class UserUpdate(BaseModel):
    """Schema for updating an existing user.

    All fields are optional to allow partial updates.

    Attributes:
        username: New username if updating.
        email: New email if updating.
        full_name: New full name if updating.
        role: New role if updating.
        is_active: New active status if updating.
        password: New password if updating (will be hashed).
    """

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = Field(None, pattern="^(admin|user)$")
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """Schema for user responses.

    Excludes password_hash for security. Includes timestamps.

    Attributes:
        id: Unique user identifier.
        created_at: Account creation timestamp.
        updated_at: Last update timestamp.
    """

    id: int = Field(..., description="Unique user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Schema for paginated user list response.

    Attributes:
        users: List of users.
        total: Total number of users in database.
        page: Current page number.
        page_size: Number of users per page.
    """

    users: list[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total users count")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Users per page")

    model_config = ConfigDict(from_attributes=True)
