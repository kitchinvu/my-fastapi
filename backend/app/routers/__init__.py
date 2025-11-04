"""API routers package."""

from .users import router as users_router
from .post import router as posts_router
from .files import router as files_router
from .auth import router as auth_router

__all__ = ["users_router", "posts_router", "files_router", "auth_router"]
