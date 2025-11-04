"""User database model."""

import enum
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class UserRole(str, enum.Enum):
    """User role enumeration.

    Attributes:
        ADMIN: Administrator role with elevated privileges.
        USER: Standard user role.
    """

    ADMIN = "admin"
    USER = "user"


class User(Base):
    """User model for database storage.

    Attributes:
        id: Unique identifier for the user.
        username: Unique username (3-50 characters).
        email: Unique email address.
        password_hash: Bcrypt hashed password.
        full_name: Optional full name of the user.
        role: User role (admin or user).
        is_active: Whether the user account is active.
        created_at: Timestamp when the user was created.
        updated_at: Timestamp when the user was last updated.
    """

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # User credentials
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # User information
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),  # Auto-update on modifications
        nullable=False
    )

    def __repr__(self) -> str:
        """String representation of User.

        Returns:
            String representation showing username and email.
        """
        return f"<User(username='{self.username}', email='{self.email}')>"
