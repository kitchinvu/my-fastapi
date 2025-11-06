"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import engine, Base
from .routers import users_router, posts_router, files_router, auth_router

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="User Management REST API with CRUD operations",
    debug=settings.DEBUG
)
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    """Create database tables on application startup.

    This creates all tables defined in SQLAlchemy models.
    For production, consider using Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    """Health check endpoint.

    Returns:
        Health status of the API.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.API_VERSION
    }

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(files_router)