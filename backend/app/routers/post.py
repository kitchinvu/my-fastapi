"""Post CRUD API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, List

from ..database import get_db
from ..schemas.post import PostCreate, PostUpdate, PostResponse, PostListResponse
from ..models.post import Post

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Annotated[Session, Depends(get_db)]
) -> Post:
    """Create a new post.

    Args:
        post: Post data to create.
        db: Database session.

    Returns:
        Created post data.
    """
    db_post = Post(**post.model_dump(), user_id=1)  # Assuming user_id=1 for simplicity
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=PostListResponse)
def list_posts(
    skip: int = Query(0, ge=0, description="Number of posts to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of posts to return"),
    db: Annotated[Session, Depends(get_db)] = None
) -> PostListResponse:
    """List posts with pagination.

    Args:
        skip: Number of posts to skip.
        limit: Maximum number of posts to return.
        db: Database session.

    Returns:
        Paginated list of posts.
    """
    total = db.query(Post).count()
    posts = db.query(Post).offset(skip).limit(limit).all()
    page = (skip // limit) + 1 if limit > 0 else 1
    return PostListResponse(posts=posts, total=total, page=page, page_size=limit)

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> Post:
    """Retrieve a post by ID.

    Args:
        post_id: ID of the post to retrieve.
        db: Database session.

    Returns:
        The requested post data.

    Raises:
        HTTPException: If the post is not found.
    """
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return db_post 

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Annotated[Session, Depends(get_db)]
) -> Post:
    """Update an existing post.

    Args:
        post_id: ID of the post to update.
        post_update: Data to update the post with.
        db: Database session.

    Returns:
        The updated post data.

    Raises:
        HTTPException: If the post is not found.
    """
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    for field, value in post_update.model_dump(exclude_unset=True).items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> None:
    """Delete a post by ID.

    Args:
        post_id: ID of the post to delete.
        db: Database session.

    Raises:
        HTTPException: If the post is not found.
    """
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    db_post.status = "deleted"
    db.commit()
