# User Management API - Planning Document

## Project Overview
A production-ready User Management REST API built with FastAPI, MySQL, and Docker. Provides complete CRUD operations with proper validation, security, and comprehensive testing.

## Architecture Decisions

### Technology Stack
- **Framework**: FastAPI 0.104+ (chosen for async support, automatic API docs, and excellent performance)
- **Database**: MySQL 8.0 (reliable, widely-used, good for relational data)
- **ORM**: SQLAlchemy 2.0 (latest version with improved typing support)
- **Validation**: Pydantic v2 (data validation and serialization)
- **Password Hashing**: passlib with bcrypt (industry standard, secure)
- **Package Manager**: uv (modern, fast Python package manager)
- **Containerization**: Docker + Docker Compose (easy deployment and development)

### Project Structure
```
backend/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py              # FastAPI app, startup, health check
│   ├── config.py            # Configuration management with pydantic-settings
│   ├── database.py          # SQLAlchemy setup, session management
│   ├── models/              # Database models (SQLAlchemy)
│   │   └── user.py
│   ├── schemas/             # API schemas (Pydantic)
│   │   └── user.py
│   ├── routers/             # API endpoints
│   │   └── users.py
│   └── utils/               # Utilities
│       └── security.py      # Password hashing
├── tests/                   # Pytest tests
├── pyproject.toml          # uv project config
└── .env                    # Environment variables
```

## Database Schema

### Users Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | User's username |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User's email |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| full_name | VARCHAR(100) | NULL | User's full name |
| role | ENUM('admin', 'user') | NOT NULL, DEFAULT 'user' | User role |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account status |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE | Last update timestamp |

### Indexes
- Primary key on `id`
- Unique index on `username`
- Unique index on `email`

## API Endpoints

### User Management
- `POST /api/v1/users` - Create new user
  - Request: UserCreate schema
  - Response: 201 Created, UserResponse
  - Errors: 409 Conflict (duplicate), 422 Validation Error

- `GET /api/v1/users` - List users with pagination
  - Query params: skip (default: 0), limit (default: 10, max: 100)
  - Response: 200 OK, UserListResponse with pagination metadata

- `GET /api/v1/users/{user_id}` - Get user by ID
  - Response: 200 OK, UserResponse
  - Errors: 404 Not Found

- `PUT /api/v1/users/{user_id}` - Update user
  - Request: UserUpdate schema (all fields optional)
  - Response: 200 OK, UserResponse
  - Errors: 404 Not Found, 409 Conflict (duplicate)

- `DELETE /api/v1/users/{user_id}` - Delete user
  - Response: 204 No Content
  - Errors: 404 Not Found

### Health Check
- `GET /health` - Health check endpoint
  - Response: 200 OK, {"status": "healthy"}

## Security Considerations

### Password Handling
- **Never store plain text passwords**
- Use passlib with bcrypt scheme (14 rounds by default)
- Hash passwords immediately upon user creation
- Never return password_hash in API responses

### Input Validation
- Email format validation using Pydantic EmailStr
- Username: 3-50 characters
- Password: minimum 8 characters
- Role validation: only 'admin' or 'user'

### Database Security
- Use environment variables for credentials
- Connection pooling with pool_pre_ping for stale connection detection
- Case-insensitive email/username uniqueness checks

## Docker Configuration

### Services
1. **MySQL**: Database service with health check
2. **FastAPI**: Application service that waits for MySQL to be healthy

### Key Points
- MySQL must be fully ready before FastAPI starts
- Use `depends_on` with `condition: service_healthy`
- Health check: `mysqladmin ping`
- Persistent volume for MySQL data
- Shared network between services

## Testing Strategy

### Unit Tests (pytest)
- Test each CRUD endpoint (success cases)
- Test error cases (404, 409, 422)
- Test password hashing (never plain text)
- Test password_hash exclusion from responses
- Test pagination logic and metadata
- **Minimum 15 tests required**

### Test Database
- Use SQLite in-memory for fast unit tests
- Override get_db dependency in tests
- Clean database between tests

### Integration Tests
- Docker Compose up with real MySQL
- Test actual HTTP endpoints
- Verify end-to-end functionality

## Development Workflow

1. **Setup**: Use uv to manage dependencies
2. **Development**: `uv run python ...` or activate venv with `source .venv/bin/activate`
3. **Code Style**: Use ruff for linting (auto-fix enabled)
4. **Type Checking**: Use mypy for static type checking
5. **Testing**: Run pytest with coverage before commits
6. **Docker**: Test with docker-compose before deployment

## Constraints and Rules (from CLAUDE.md)

- ✅ Maximum 500 lines per file
- ✅ Google-style docstrings for all functions
- ✅ Type hints everywhere
- ✅ Relative imports within app package
- ✅ Use python-dotenv for environment variables
- ✅ Create pytest tests for all features
- ✅ Update TASK.md when completing work

## Future Enhancements

- [ ] JWT authentication for secure endpoints
- [ ] Alembic migrations for schema management
- [ ] Rate limiting
- [ ] API versioning
- [ ] Logging and monitoring
- [ ] Password reset functionality
- [ ] Email verification
- [ ] Role-based access control (RBAC)
- [ ] Soft delete instead of hard delete
- [ ] Audit trail for user changes

## Version History

- **v1.0.0** (2025-10-29): Initial implementation with basic CRUD operations
