# User Management API

A production-ready User Management REST API built with FastAPI, MySQL, and Docker.

> 📘 **สำหรับ Junior Developers:** อ่าน [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) สำหรับคู่มือการพัฒนาแบบละเอียด

## Features

- ✅ Complete CRUD operations for users
- ✅ Password hashing with bcrypt
- ✅ Email validation
- ✅ Pagination support
- ✅ MySQL database with SQLAlchemy 2.0
- ✅ Docker and Docker Compose support
- ✅ Comprehensive test coverage (18+ tests)
- ✅ Type hints and validation with Pydantic v2
- ✅ Auto-generated API documentation

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **Password Hashing**: passlib + bcrypt
- **Package Manager**: uv
- **Testing**: pytest
- **Containerization**: Docker + Docker Compose

## Prerequisites

**Option 1: Docker Only** (Simplest)
- Docker and Docker Compose
- Git

**Option 2: Full Development Setup** (Recommended)
- Docker and Docker Compose
- Python 3.11+
- uv package manager
- Git

> 💡 ดูรายละเอียดใน [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md#1-การติดตั้งโปรแกรมและ-dependencies)

## Installation

### 1. Clone the repository

```bash
cd backend
```

### 2. Install dependencies with uv

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
uv sync
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

### Option 1: Run with uv (Development)

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the application
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Option 2: Run with Docker Compose (Recommended)

```bash
# From the project root directory
docker-compose up --build
```

This will start:
- MySQL database on port 3306
- FastAPI application on port 8000

## API Endpoints

### Health Check
- `GET /health` - Check API health status

### User Management
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users` - List users (with pagination)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example API Calls

### Create a user

```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "full_name": "John Doe",
    "role": "user"
  }'
```

### List users with pagination

```bash
curl http://localhost:8000/api/v1/users?skip=0&limit=10
```

### Get user by ID

```bash
curl http://localhost:8000/api/v1/users/1
```

### Update user

```bash
curl -X PUT http://localhost:8000/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Updated Doe"
  }'
```

### Delete user

```bash
curl -X DELETE http://localhost:8000/api/v1/users/1
```

## Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=app --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_users.py -v
```

## Development

### Code Style and Linting

```bash
# Check code style
uv run ruff check app/ tests/

# Auto-fix issues
uv run ruff check app/ tests/ --fix
```

### Type Checking

```bash
uv run mypy app/
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models/              # SQLAlchemy models
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas
│   │   └── user.py
│   ├── routers/             # API endpoints
│   │   └── users.py
│   └── utils/               # Utilities
│       └── security.py
├── tests/                   # Pytest tests
│   ├── conftest.py
│   └── test_users.py
├── pyproject.toml          # uv project config
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://...` |
| `PROJECT_NAME` | API project name | `User Management API` |
| `DEBUG` | Debug mode | `True` |
| `API_VERSION` | API version | `1.0.0` |

## Security Notes

- Passwords are hashed using bcrypt before storage
- Password hashes are never returned in API responses
- Email addresses are validated using Pydantic EmailStr
- All inputs are validated with Pydantic schemas

## Future Enhancements

- [ ] JWT authentication
- [ ] Alembic migrations
- [ ] Rate limiting
- [ ] Role-based access control (RBAC)
- [ ] Password reset functionality
- [ ] Email verification
- [ ] API key authentication

## License

This project is created as part of the Context Engineering Template.

## Documentation

See [PLANNING.md](../PLANNING.md) for architecture decisions and detailed planning.
See [TASK.md](../TASK.md) for task tracking and completion status.
