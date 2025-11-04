"""User CRUD API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated

from ..database import get_db
from ..schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from ..models.user import User
from ..utils.security import hash_password

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """Create a new user.

    Args:
        user: User data to create.
        db: Database session.

    Returns:
        Created user data.

    Raises:
        HTTPException: 409 if username or email already exists.
    """
    # Check for duplicate username or email
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()

    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # Hash password before storing
    hashed_password = hash_password(user.password)

    # Create user instance
    db_user = User(
        **user.model_dump(exclude={"password"}),
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/", response_model=UserListResponse)
def list_users(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    db: Annotated[Session, Depends(get_db)] = None
) -> dict:
    """List users with pagination.

    Args:
        skip: Number of users to skip (offset).
        limit: Maximum number of users to return (max 100).
        db: Database session.

    Returns:
        Paginated list of users with metadata.
    """
    # Get total count
    total = db.query(User).count()

    # Get paginated users
    users = db.query(User).offset(skip).limit(limit).all()

    # Calculate page number
    page = (skip // limit) + 1 if limit > 0 else 1

    return {
        "users": users,
        "total": total,
        "page": page,
        "page_size": limit
    }


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """Get a user by ID.

    Args:
        user_id: The ID of the user to retrieve.
        db: Database session.

    Returns:
        User data.

    Raises:
        HTTPException: 404 if user not found.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """Update a user by ID.

    Args:
        user_id: The ID of the user to update.
        user_update: Updated user data (all fields optional).
        db: Database session.

    Returns:
        Updated user data.

    Raises:
        HTTPException: 404 if user not found, 409 if duplicate username/email.
    """
    # Get existing user
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    # Get update data (exclude None values)
    update_data = user_update.model_dump(exclude_unset=True)

    # Check for duplicate username/email if being updated
    if "username" in update_data or "email" in update_data:
        existing = db.query(User).filter(
            User.id != user_id,
            (
                (User.username == update_data.get("username")) |
                (User.email == update_data.get("email"))
            )
        ).first()

        if existing:
            if existing.username == update_data.get("username"):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

    # Hash password if being updated
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    # Update user attributes
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> None:
    """Delete a user by ID.

    Args:
        user_id: The ID of the user to delete.
        db: Database session.

    Raises:
        HTTPException: 404 if user not found.
    """
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    db.delete(db_user)
    db.commit()
