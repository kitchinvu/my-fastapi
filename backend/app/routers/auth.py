"""Authentication endpoints."""
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt

from app.schemas.auth import LoginRequest, TokenResponse
from app.database import get_db
from app.models.user import User
from app.utils.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    credentials: LoginRequest,
    db: Annotated[Session, Depends(get_db)]
) -> TokenResponse:
    """Login endpoint - authenticate user and return JWT token.
    
    Args:
        credentials: Login credentials (username and password).
        db: Database session.
        
    Returns:
        TokenResponse with access_token and token_type.
        
    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    # Find user by username
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not bcrypt.checkpw(
        credentials.password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer")