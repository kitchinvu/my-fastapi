"""Authentication dependencies."""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.jwt import verify_access_token

# Security scheme for bearer token
security = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Authorization credentials (Bearer token).
        db: Database session.
        
    Returns:
        Current authenticated User object.
        
    Raises:
        HTTPException: 401 if token is invalid or user not found.
    """
    token = credentials.credentials
    
    # Verify token and get payload
    payload = verify_access_token(token)
    
    # Get user_id from token payload
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user