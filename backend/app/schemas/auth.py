"""Authentication schemas."""
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    """Login request schema.
    
    Attributes:
        username: User's username.
        password: User's password.
    """
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class TokenResponse(BaseModel):
    """Token response schema.
    
    Attributes:
        access_token: JWT access token.
        token_type: Type of the token (e.g., Bearer).
    """
    access_token: str
    token_type: str = "bearer"