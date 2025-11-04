## FEATURE:

Build a User Management REST API using FastAPI with MySQL database and Docker deployment.

### Core Requirements:
- **CRUD Operations**: Create, Read, List (with pagination), Update, Delete users
- **User Model Fields**:
  - `id` (Primary Key, Auto-increment)
  - `username` (Unique, Required)
  - `email` (Unique, Required, Email validation)
  - `password_hash` (Hashed password storage)
  - `full_name` (Optional)
  - `role` (Enum: "admin", "user")
  - `is_active` (Boolean, default: True)
  - `created_at` (Auto-generated timestamp)
  - `updated_at` (Auto-updated timestamp)

### API Endpoints:
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users with pagination
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user
- `GET /health` - Health check

### Technical Stack:
- FastAPI (latest stable)
- MySQL 8.0
- SQLAlchemy ORM
- Pydantic v2 for validation
- passlib + bcrypt for password hashing
- python-dotenv for environment variables
- Docker + Docker Compose

### Project Structure:
```
my-fastapi/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/user.py
│   ├── schemas/user.py
│   └── routers/users.py
├── tests/test_users.py
├── venv_linux/
├── .env
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## EXAMPLES:

No specific examples provided. Follow FastAPI best practices:
- Separate models, schemas, and routers
- Use dependency injection for database sessions
- Proper error handling with HTTPException
- Type hints throughout the code

## DOCUMENTATION:

Reference these resources during development:

- **FastAPI**: https://fastapi.tiangolo.com/
- **FastAPI SQL Databases**: https://fastapi.tiangolo.com/tutorial/sql-databases/
- **SQLAlchemy 2.0**: https://docs.sqlalchemy.org/en/20/
- **Pydantic v2**: https://docs.pydantic.dev/latest/
- **MySQL Docker**: https://hub.docker.com/_/mysql
- **passlib**: https://passlib.readthedocs.io/en/stable/
- **Docker Compose**: https://docs.docker.com/compose/

## OTHER CONSIDERATIONS:

### Security:
- Never store plain text passwords - always hash with bcrypt
- Don't return password_hash in API responses
- Validate email format using Pydantic EmailStr
- Handle duplicate username/email with 409 Conflict status

### Database:
- Use proper indexes on username and email fields
- Implement connection pooling
- Handle database connection errors gracefully
- Ensure updated_at timestamp updates on modifications

### API Design:
- Return proper HTTP status codes (200, 201, 204, 400, 404, 409, 500)
- Include pagination metadata in list responses
- Consistent error response format
- Validate user_id exists before UPDATE/DELETE

### Docker:
- MySQL must be ready before FastAPI starts (use health checks)
- Include .dockerignore file
- Set proper environment variables in docker-compose
- Persistent volume for MySQL data

### Testing:
- Pytest tests for all endpoints
- Test success and failure cases
- Test duplicate username/email handling
- Test pagination edge cases

### Common Gotchas:
- Always use venv_linux for Python commands
- Handle case sensitivity for username/email
- Close database sessions properly
- Create .env.example file (without sensitive values)
- Wait for MySQL to be ready in Docker
