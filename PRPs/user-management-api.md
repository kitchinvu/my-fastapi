name: "User Management REST API with FastAPI, MySQL, and Docker"
description: |

## Purpose
Build a production-ready User Management REST API from scratch using FastAPI, MySQL database, and Docker containerization. The system provides complete CRUD operations with proper validation, security, and testing.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from best practices
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Follow all rules in CLAUDE.md strictly

---

## Goal
Create a fully functional User Management API with FastAPI backend, MySQL database, Docker deployment, comprehensive testing, and proper security measures for password handling.

## Why
- **Business value**: Provides foundational user management system that can be extended
- **Learning**: Demonstrates FastAPI + SQLAlchemy + Docker best practices
- **Problems solved**: Complete CRUD operations with validation, security, and containerization

## What
A REST API with the following capabilities:
- Create users with validation and password hashing
- List users with pagination support
- Retrieve individual user details
- Update user information
- Delete users
- Health check endpoint for monitoring
- Fully containerized with Docker Compose

### Success Criteria
- [ ] All CRUD endpoints working correctly
- [ ] Password hashing with bcrypt (never plain text)
- [ ] Pagination working with metadata
- [ ] Docker Compose starts both FastAPI and MySQL
- [ ] All pytest tests passing (minimum 3 tests per endpoint)
- [ ] No type errors (mypy passes)
- [ ] Proper HTTP status codes returned
- [ ] Database indexes on username and email

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window

- url: https://fastapi.tiangolo.com/
  why: Core FastAPI concepts and patterns
  critical: Request/Response models, dependency injection

- url: https://fastapi.tiangolo.com/tutorial/sql-databases/
  why: SQLAlchemy integration with FastAPI
  critical: Database session management, dependency injection pattern

- url: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
  why: SQLAlchemy 2.0 declarative models
  critical: Using mapped_column, relationship patterns

- url: https://docs.pydantic.dev/latest/concepts/models/
  why: Pydantic v2 model creation and validation
  critical: Field validation, EmailStr, ConfigDict

- url: https://docs.pydantic.dev/latest/api/types/
  why: Pydantic types for email validation
  critical: EmailStr type for email validation

- url: https://passlib.readthedocs.io/en/stable/narr/hash-tutorial.html
  why: Password hashing with bcrypt
  critical: CryptContext setup, hash and verify methods

- url: https://docs.docker.com/compose/compose-file/
  why: Docker Compose configuration
  critical: depends_on, healthcheck, volumes, environment variables

- url: https://hub.docker.com/_/mysql
  why: MySQL Docker image configuration
  critical: Environment variables, health check command
```

### Current Codebase Tree
```bash
/Users/kit/Desktop/workspace/my-fastapi/
├── CLAUDE.md                    # Project rules (MUST FOLLOW)
├── INITIAL.md                   # Feature requirements
├── README.md                    # Template documentation
├── .gitignore                   # Git ignore file
├── examples/                    # Empty - no existing patterns
└── PRPs/                        # This PRP location
```

### Desired Codebase Tree with Files to be Added
```bash
/Users/kit/Desktop/workspace/my-fastapi/
├── app/
│   ├── __init__.py              # Package init
│   ├── main.py                  # FastAPI app entry point, router registration
│   ├── config.py                # Configuration using pydantic-settings
│   ├── database.py              # SQLAlchemy engine, session, Base
│   ├── models/
│   │   ├── __init__.py          # Export models
│   │   └── user.py              # SQLAlchemy User model with all fields
│   ├── schemas/
│   │   ├── __init__.py          # Export schemas
│   │   └── user.py              # Pydantic schemas (Create, Update, Response, List)
│   ├── routers/
│   │   ├── __init__.py          # Export routers
│   │   └── users.py             # User CRUD endpoints
│   └── utils/
│       ├── __init__.py          # Export utilities
│       └── security.py          # Password hashing functions
├── tests/
│   ├── __init__.py              # Package init
│   ├── conftest.py              # Pytest fixtures (test database, client)
│   └── test_users.py            # User endpoint tests (15+ tests)
├── venv_linux/                  # Virtual environment (create this)
├── .env                         # Environment variables (gitignored)
├── .env.example                 # Example env vars (commit this)
├── .dockerignore                # Docker ignore file
├── Dockerfile                   # FastAPI container definition
├── docker-compose.yml           # Multi-container orchestration
├── requirements.txt             # Python dependencies
├── PLANNING.md                  # Architecture and decisions (create this)
├── TASK.md                      # Task tracking (create this)
└── README.md                    # Updated with setup instructions
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: Always use venv_linux for ALL Python commands (per CLAUDE.md)
# Example: source venv_linux/bin/activate && python -m pytest

# CRITICAL: SQLAlchemy 2.0 uses mapped_column instead of Column
# OLD: id = Column(Integer, primary_key=True)
# NEW: id: Mapped[int] = mapped_column(primary_key=True)

# CRITICAL: Pydantic v2 uses ConfigDict instead of Config class
# OLD: class Config: orm_mode = True
# NEW: model_config = ConfigDict(from_attributes=True)

# CRITICAL: MySQL must be healthy before FastAPI starts
# Use healthcheck in docker-compose and depends_on with condition: service_healthy

# CRITICAL: Never return password_hash in response schemas
# Exclude it explicitly in Pydantic schemas

# CRITICAL: Updated_at must auto-update on modifications
# Use onupdate=func.now() in SQLAlchemy column definition

# CRITICAL: Email uniqueness check must be case-insensitive
# MySQL default collation is case-insensitive, but validate in code too

# CRITICAL: File size limit from CLAUDE.md - max 500 lines per file
# Keep routers, models, schemas concise

# CRITICAL: Use python-dotenv load_dotenv() as per CLAUDE.md
# Load in config.py before reading environment variables

# CRITICAL: All functions need Google-style docstrings (CLAUDE.md requirement)

# CRITICAL: Type hints everywhere (CLAUDE.md requirement)
# Use from typing import Optional, List for compatibility

# CRITICAL: Use relative imports within app package (CLAUDE.md)
# from ..models import user (not from app.models import user)
```

## Implementation Blueprint

### Data Models and Structure

```python
# app/models/user.py - SQLAlchemy ORM Model
from sqlalchemy import String, Boolean, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"

class User(Base):
    """User model for database."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()  # CRITICAL: Auto-update timestamp
    )


# app/schemas/user.py - Pydantic Schemas
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # CRITICAL: Use EmailStr for validation
    full_name: Optional[str] = Field(None, max_length=100)
    role: str = Field(default="user", pattern="^(admin|user)$")
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    """Schema for updating a user (all fields optional)."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = Field(None, pattern="^(admin|user)$")
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    """Schema for user responses (excludes password_hash)."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2

class UserListResponse(BaseModel):
    """Schema for paginated user list."""
    users: list[UserResponse]
    total: int
    page: int
    page_size: int

    model_config = ConfigDict(from_attributes=True)
```

### List of Tasks in Order

```yaml
Task 1: Project Setup and Configuration
CREATE venv_linux/:
  - Run: python3 -m venv venv_linux
  - Activate: source venv_linux/bin/activate
  - Required by CLAUDE.md

CREATE requirements.txt:
  - fastapi>=0.104.0
  - uvicorn[standard]>=0.24.0
  - sqlalchemy>=2.0.0
  - pymysql>=1.1.0
  - cryptography>=41.0.0  # Required for pymysql
  - pydantic>=2.5.0
  - pydantic-settings>=2.1.0
  - python-dotenv>=1.0.0
  - passlib[bcrypt]>=1.7.4
  - pytest>=7.4.0
  - pytest-asyncio>=0.21.0
  - httpx>=0.25.0  # For testing

CREATE .env.example:
  - Template for environment variables
  - No sensitive values

CREATE .dockerignore:
  - venv_linux/
  - __pycache__/
  - *.pyc
  - .env
  - .git/
  - tests/
  - *.md

CREATE PLANNING.md:
  - Document architecture decisions
  - API endpoint structure
  - Database schema
  - Security considerations
  - Required by CLAUDE.md

CREATE TASK.md:
  - List: "Create User Management API - 2025-10-29"
  - Required by CLAUDE.md

Task 2: Configuration and Database Setup
CREATE app/__init__.py:
  - Empty file for package

CREATE app/config.py:
  - Use pydantic-settings BaseSettings
  - Load environment variables with load_dotenv()
  - Provide defaults for development
  - Validate required fields

CREATE app/database.py:
  - SQLAlchemy engine with pymysql
  - SessionLocal factory
  - Base declarative class
  - get_db() dependency function
  - Connection string from config

Task 3: Security Utilities
CREATE app/utils/__init__.py:
  - Export security functions

CREATE app/utils/security.py:
  - PATTERN: Use passlib CryptContext
  - hash_password(plain: str) -> str
  - verify_password(plain: str, hashed: str) -> bool
  - Use bcrypt scheme
  - Add docstrings (Google style)

Task 4: Database Models
CREATE app/models/__init__.py:
  - Export User model

CREATE app/models/user.py:
  - PATTERN: SQLAlchemy 2.0 declarative with Mapped
  - UserRole enum (admin, user)
  - User model with all fields
  - Indexes on username and email
  - onupdate for updated_at
  - Google-style docstrings

Task 5: Pydantic Schemas
CREATE app/schemas/__init__.py:
  - Export all schemas

CREATE app/schemas/user.py:
  - UserBase, UserCreate, UserUpdate schemas
  - UserResponse (excludes password_hash)
  - UserListResponse with pagination metadata
  - Field validations (min_length, EmailStr, pattern)
  - ConfigDict(from_attributes=True) for Pydantic v2

Task 6: User CRUD Router
CREATE app/routers/__init__.py:
  - Export user router

CREATE app/routers/users.py:
  - PATTERN: FastAPI APIRouter with prefix="/api/v1/users"
  - POST / - Create user (hash password, handle duplicates)
  - GET / - List users with pagination (query params: skip, limit)
  - GET /{user_id} - Get single user
  - PUT /{user_id} - Update user (hash password if provided)
  - DELETE /{user_id} - Delete user
  - Dependency injection: db: Session = Depends(get_db)
  - Proper HTTP status codes (200, 201, 204, 404, 409, 500)
  - Error handling with HTTPException
  - Docstrings for all endpoints

Task 7: FastAPI Application
CREATE app/main.py:
  - Create FastAPI() instance
  - Include health check: GET /health
  - Include user router
  - CORS middleware (if needed)
  - Create database tables on startup
  - Graceful error handling
  - API metadata (title, version, description)

Task 8: Docker Configuration
CREATE Dockerfile:
  - Use python:3.11-slim base image
  - Set working directory /app
  - Copy requirements and install
  - Copy app code
  - Expose port 8000
  - CMD: uvicorn app.main:app --host 0.0.0.0 --port 8000

CREATE docker-compose.yml:
  - mysql service:
    - image: mysql:8.0
    - environment: MYSQL_ROOT_PASSWORD, MYSQL_DATABASE
    - volumes: persistent data
    - healthcheck: mysqladmin ping
  - fastapi service:
    - build from Dockerfile
    - depends_on mysql (condition: service_healthy)
    - environment: DATABASE_URL
    - ports: 8000:8000
  - networks: shared network

Task 9: Comprehensive Testing
CREATE tests/__init__.py:
  - Empty file

CREATE tests/conftest.py:
  - PATTERN: Pytest fixtures
  - test_db fixture with SQLite in-memory
  - client fixture using TestClient
  - Override get_db dependency
  - Setup and teardown

CREATE tests/test_users.py:
  - Test create user (success)
  - Test create user duplicate username (409)
  - Test create user duplicate email (409)
  - Test create user invalid email (422)
  - Test get user by id (success)
  - Test get user not found (404)
  - Test list users with pagination
  - Test list users empty
  - Test update user (success)
  - Test update user not found (404)
  - Test delete user (success)
  - Test delete user not found (404)
  - Test password is hashed (not plain text)
  - Test password_hash not in response
  - Test pagination metadata
  - MINIMUM 15 tests total (per CLAUDE.md: success, edge, failure)

Task 10: Documentation
UPDATE README.md:
  - Project overview
  - Features list
  - Tech stack
  - Prerequisites (Docker, Docker Compose)
  - Installation steps
  - Configuration (.env setup)
  - Running with Docker
  - Running tests
  - API endpoints documentation
  - Example API calls (curl)
```

### Key Implementation Details

```python
# app/database.py - Database Session Management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# PATTERN: Connection string with pymysql
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # CRITICAL: Test connections before using
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency for database sessions.

    Yields:
        Session: Database session that auto-closes after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# app/routers/users.py - Example CRUD Endpoints
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import user as schemas
from ..models import user as models
from ..utils.security import hash_password

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user: User data to create.
        db: Database session.

    Returns:
        Created user data.

    Raises:
        HTTPException: 409 if username or email already exists.
    """
    # CRITICAL: Check for duplicates
    existing = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.email)
    ).first()

    if existing:
        if existing.username == user.username:
            raise HTTPException(status_code=409, detail="Username already exists")
        raise HTTPException(status_code=409, detail="Email already exists")

    # CRITICAL: Hash password before storing
    hashed_password = hash_password(user.password)

    db_user = models.User(
        **user.model_dump(exclude={"password"}),
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/", response_model=schemas.UserListResponse)
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    List users with pagination.

    Args:
        skip: Number of users to skip.
        limit: Maximum number of users to return.
        db: Database session.

    Returns:
        Paginated list of users with metadata.
    """
    # CRITICAL: Limit maximum page size
    limit = min(limit, 100)

    total = db.query(models.User).count()
    users = db.query(models.User).offset(skip).limit(limit).all()

    return {
        "users": users,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit
    }


# docker-compose.yml - Complete Configuration
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: fastapi_mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: user_management
      MYSQL_USER: fastapi_user
      MYSQL_PASSWORD: fastapi_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app_network

  fastapi:
    build: .
    container_name: fastapi_app
    depends_on:
      mysql:
        condition: service_healthy  # CRITICAL: Wait for MySQL
    environment:
      DATABASE_URL: mysql+pymysql://fastapi_user:fastapi_password@mysql:3306/user_management
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app  # Hot reload in development
    networks:
      - app_network

volumes:
  mysql_data:

networks:
  app_network:
    driver: bridge
```

### Integration Points
```yaml
ENVIRONMENT VARIABLES (.env):
  DATABASE_URL: mysql+pymysql://user:password@localhost:3306/dbname
  PROJECT_NAME: "User Management API"
  DEBUG: "True"

DOCKER:
  - MySQL ready before FastAPI (healthcheck + depends_on)
  - Persistent volume for data
  - Shared network between services

DATABASE MIGRATIONS (Future):
  - Consider Alembic for production
  - For now: create tables on app startup
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# CRITICAL: Always activate venv_linux first (CLAUDE.md requirement)
source venv_linux/bin/activate

# Install dependencies
pip install -r requirements.txt

# Check code style and auto-fix
python -m ruff check app/ tests/ --fix

# Type checking
python -m mypy app/

# Expected: No errors. If errors exist, READ and FIX them.
```

### Level 2: Unit Tests
```bash
# CRITICAL: Use venv_linux (CLAUDE.md requirement)
source venv_linux/bin/activate

# Run all tests with coverage
python -m pytest tests/ -v --cov=app --cov-report=term-missing

# Expected: All tests pass, >80% coverage
# If failing: Read error, understand root cause, fix code, re-run

# Run specific test file
python -m pytest tests/test_users.py -v

# Run specific test
python -m pytest tests/test_users.py::test_create_user -v
```

### Level 3: Integration Test with Docker
```bash
# Build and start services
docker-compose up --build

# Wait for MySQL to be healthy (check logs)
docker-compose logs mysql

# Test health endpoint
curl http://localhost:8000/health

# Expected: {"status": "healthy"}

# Test create user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "full_name": "Test User"
  }'

# Expected: 201 Created with user data (no password_hash in response)

# Test list users
curl http://localhost:8000/api/v1/users?skip=0&limit=10

# Expected: {"users": [...], "total": 1, "page": 1, "page_size": 10}

# Test get user by ID
curl http://localhost:8000/api/v1/users/1

# Expected: User data without password_hash

# Cleanup
docker-compose down -v
```

## Final Validation Checklist
- [ ] All tests pass: `source venv_linux/bin/activate && python -m pytest tests/ -v`
- [ ] No linting errors: `python -m ruff check app/ tests/`
- [ ] No type errors: `python -m mypy app/`
- [ ] Docker Compose builds successfully
- [ ] MySQL service becomes healthy
- [ ] FastAPI service starts after MySQL
- [ ] Health endpoint returns 200
- [ ] Create user returns 201 with hashed password
- [ ] Password_hash NOT in API responses
- [ ] Duplicate username returns 409
- [ ] Duplicate email returns 409
- [ ] List users includes pagination metadata
- [ ] Get user by ID returns 404 for non-existent user
- [ ] Update user updates updated_at timestamp
- [ ] All files under 500 lines (CLAUDE.md requirement)
- [ ] All functions have Google-style docstrings
- [ ] PLANNING.md created and up-to-date
- [ ] TASK.md created with completion date
- [ ] README.md updated with setup instructions
- [ ] .env.example includes all required variables

---

## Anti-Patterns to Avoid
- ❌ Don't store plain text passwords - always hash with bcrypt
- ❌ Don't return password_hash in API responses
- ❌ Don't skip MySQL health check in docker-compose
- ❌ Don't forget to activate venv_linux for Python commands
- ❌ Don't create files over 500 lines (refactor if needed)
- ❌ Don't skip docstrings on functions
- ❌ Don't use Column() syntax - use mapped_column() for SQLAlchemy 2.0
- ❌ Don't use orm_mode=True - use ConfigDict(from_attributes=True) for Pydantic v2
- ❌ Don't hardcode database credentials - use environment variables
- ❌ Don't skip the updated_at auto-update (use onupdate=func.now())
- ❌ Don't forget to create PLANNING.md and TASK.md (CLAUDE.md requirement)
- ❌ Don't use absolute imports within app package - use relative imports

## Confidence Score: 8/10

**High confidence due to:**
- Clear, well-defined requirements
- Standard FastAPI + SQLAlchemy patterns
- Comprehensive documentation available
- Explicit CLAUDE.md rules to follow
- Well-structured validation gates

**Minor uncertainties:**
- First-time Docker Compose MySQL health check timing (might need adjustment)
- Exact MySQL connection string format with pymysql (documentation provides guidance)
- venv_linux activation in different shell environments (standard Python venv)

**Mitigation:**
- Extensive testing loops will catch and fix any issues
- Documentation URLs provide authoritative guidance
- Progressive validation ensures working code at each step
