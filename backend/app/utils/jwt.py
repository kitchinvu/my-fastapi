"""JWT token utilities."""
import jwt
from datetime import datetime, timedelta
from app.config import settings
from typing import Optional
from fastapi import HTTPException, status

# Secret key สำหรับ sign JWT (อ่านจาก environment variable)
SECRET_KEY = settings.JWT_SECRET_KEY
# Algorithm ที่ใช้ในการ sign JWT
ALGORITHM = settings.JWT_ALGORITHM
# ระยะเวลาหมดอายุของ token (นาที)
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """สร้าง JWT access token.

    Args:
        data (dict): ข้อมูลที่จะเก็บใน token.
        expires_delta (Optional[timedelta]): ระยะเวลาหมดอายุของ token.

    Returns:
        str: JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    """ตรวจสอบความถูกต้องของ JWT access token.

    Args:
        token (str): JWT access token.

    Returns:
        dict: ข้อมูลที่เก็บใน token.

    Raises:
        HTTPException: 401 หาก token ไม่ถูกต้องหรือหมดอายุ.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    