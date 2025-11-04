# 📘 Developer Guide - User Management API

คู่มือสำหรับ Junior Developer ที่เพิ่งเข้ามาพัฒนาโปรเจกต์ User Management API

---

## 📑 สารบัญ

1. [การติดตั้งโปรแกรมและ Dependencies](#1-การติดตั้งโปรแกรมและ-dependencies)
2. [การ Start Project](#2-การ-start-project)
3. [โครงสร้าง Project](#3-โครงสร้าง-project)
4. [การไล่ Code: Request → Database → Response](#4-การไล่-code-request--database--response)
5. [การเข้าดูข้อมูลใน Database](#5-การเข้าดูข้อมูลใน-database)
6. [การติดตั้ง Library Python เพิ่มเติม](#6-การติดตั้ง-library-python-เพิ่มเติม)
7. [การ Debug และดู Logs](#7-การ-debug-และดู-logs)
8. [Authentication & Authorization](#authentication--authorization)
---

## Quick Start
```bash
git clone <repo>
cd my-fastapi/backend
cp .env.example .env    # ← สร้างไฟล์ .env
cd ..
docker compose up --build

## 1. การติดตั้งโปรแกรมและ Dependencies

### 🤔 คำถาม: ทำไมต้องติดตั้ง Python ด้วย? ใช้แค่ Docker ไม่ได้เหรอ?

**คำตอบ: ได้ครับ! แต่...**

คุณมี **2 ตัวเลือก** ในการพัฒนา:

#### ✅ **ตัวเลือกที่ 1: Docker อย่างเดียว** (ง่ายที่สุด)
- เหมาะสำหรับ: **ทดสอบ Production-like** หรือ **Deploy**
- ข้อดี: ไม่ต้องติดตั้ง Python/uv เลย
- ข้อเสีย: พัฒนาช้า, ไม่มี IDE autocomplete, debug ยาก

```bash
# ทำได้ทั้งหมดผ่าน Docker
docker compose up          # รัน API
docker compose run fastapi uv run pytest    # รัน tests
docker exec fastapi uv run ruff check app/  # linting
```

#### ⭐ **ตัวเลือกที่ 2: Python + uv + Docker** (แนะนำสำหรับ Development)
- เหมาะสำหรับ: **พัฒนาประจำวัน**
- ข้อดี: เร็ว, มี IDE support, debug ง่าย
- ข้อเสีย: ต้องติดตั้ง Python

```bash
# Development: เร็วกว่ามาก
uv run pytest tests/            # ⚡ เร็ว
uv run uvicorn app.main:app --reload

# Production Testing: ใช้ Docker
docker compose up --build       # ทดสอบแบบจริง
```

#### 📊 เปรียบเทียบ

| งาน | Docker อย่างเดียว | Python + uv + Docker |
|-----|------------------|---------------------|
| **Run API** | ✅ ใช้ได้ | ✅⚡ เร็วกว่า |
| **Run Tests** | ⚠️ ช้า | ✅⚡ เร็วมาก |
| **IDE Autocomplete** | ❌ ไม่มี | ✅ ครบ |
| **Debug Breakpoints** | ⚠️ ยาก | ✅ ง่าย |
| **Hot Reload** | 🐢 1-3 วินาที | ⚡ < 0.5 วินาที |

**คำแนะนำ:** ถ้าคุณเป็น Junior Developer ที่กำลังเรียนรู้ → แนะนำติดตั้ง Python + uv

---

### 1.1 โปรแกรมที่ต้องติดตั้ง

> **💡 หมายเหตุ:** ถ้าคุณเลือก **Docker อย่างเดียว** ติดตั้งแค่ข้อ 1 และ 4 ก็พอ (Docker + Git)

#### macOS / Linux:
```bash
# 1. ติดตั้ง Docker Desktop
# ดาวน์โหลดจาก: https://www.docker.com/products/docker-desktop

# 2. ติดตั้ง uv (Python Package Manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# เพิ่ม uv เข้า PATH
source $HOME/.local/bin/env

# 3. ติดตั้ง Python 3.11+ (ถ้ายังไม่มี)
# macOS with Homebrew:
brew install python@3.11

# 4. ติดตั้ง Git (ถ้ายังไม่มี)
brew install git
```

#### Windows:
```powershell
# 1. ติดตั้ง Docker Desktop
# ดาวน์โหลดจาก: https://www.docker.com/products/docker-desktop

# 2. ติดตั้ง uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. ติดตั้ง Python 3.11+
# ดาวน์โหลดจาก: https://www.python.org/downloads/

# 4. ติดตั้ง Git
# ดาวน์โหลดจาก: https://git-scm.com/download/win
```

### 1.2 Clone Project

```bash
# Clone repository
git clone <repository-url>
cd my-fastapi

# เข้าไปใน backend folder
cd backend
```

### 1.3 ติดตั้ง Dependencies

```bash
# ติดตั้ง dependencies ด้วย uv
uv sync

# ติดตั้ง dev dependencies (สำหรับ testing, linting)
uv sync --group dev
```

### 1.4 ตั้งค่า Environment Variables

```bash
# สร้างไฟล์ .env จาก template
cp .env.example .env

# แก้ไขไฟล์ .env ตามต้องการ (ถ้าจำเป็น)
# สำหรับ development ใช้ค่า default ได้เลย
```

---

## 2. การ Start Project

### 🎯 เลือกวิธีที่เหมาะกับคุณ

- **วิธีที่ 1 (Docker)**: เหมาะสำหรับทดสอบแบบ Production-like
- **วิธีที่ 2 (Development)**: เหมาะสำหรับเขียนโค้ดประจำวัน (ต้องมี Python)
- **วิธีที่ 3 (Docker สำหรับทุกอย่าง)**: ใช้ Docker อย่างเดียว ไม่ต้องติดตั้ง Python!

---

### 2.1 วิธีที่ 1: รันด้วย Docker (แนะนำ - Production-like Testing)

```bash
# กลับไปที่ root folder
cd ..  # จาก backend/ ไปที่ my-fastapi/

# Start ทั้ง FastAPI + MySQL
docker compose up --build

# หรือรันแบบ background
docker compose up -d --build
```

**เช็คว่า services ทำงาน:**
```bash
# ดู logs
docker compose logs -f

# ดูเฉพาะ FastAPI logs
docker compose logs -f fastapi

# ดูเฉพาะ MySQL logs
docker compose logs -f mysql

# เช็ค containers ที่กำลังทำงาน
docker compose ps
```

**หยุด services:**
```bash
# หยุด (เก็บข้อมูลไว้)
docker compose down

# หยุดและลบข้อมูลทั้งหมด
docker compose down -v
```

### 2.2 วิธีที่ 2: รันแบบ Development (ไม่ใช้ Docker)

**ต้องมี MySQL ติดตั้งอยู่ในเครื่องก่อน!**

```bash
# เข้า backend folder
cd backend

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# หรือ
.venv\Scripts\activate     # Windows

# Start server (hot reload enabled)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2.3 วิธีที่ 3: ใช้ Docker สำหรับทุกอย่าง (ไม่ต้องติดตั้ง Python!)

**สำหรับคนที่ไม่อยากติดตั้ง Python/uv บนเครื่อง**

#### 🚀 Start API
```bash
# Start API + MySQL
docker compose up --build

# API จะรันที่: http://localhost:8000
```

#### 🧪 Run Tests
```bash
# รัน tests ใน Docker container
docker compose run --rm fastapi uv run pytest tests/ -v

# Run tests with coverage
docker compose run --rm fastapi uv run pytest tests/ -v --cov=app
```

#### ✅ Linting & Type Checking
```bash
# Ruff linting
docker compose run --rm fastapi uv run ruff check app/ tests/

# Auto-fix linting issues
docker compose run --rm fastapi uv run ruff check app/ tests/ --fix

# Type checking with mypy
docker compose run --rm fastapi uv run mypy app/
```

#### 📦 ติดตั้ง Library ใหม่
```bash
# 1. เข้าไปใน container
docker compose exec fastapi bash

# 2. ติดตั้ง library
uv add <package-name>

# 3. Exit
exit

# 4. Rebuild container
docker compose up --build
```

#### 🔍 Debug & Explore
```bash
# เข้าไปใน container เพื่อ explore
docker compose exec fastapi bash

# ตอนนี้คุณอยู่ใน container แล้ว สามารถ:
ls app/                    # ดูไฟล์
cat app/main.py           # อ่านไฟล์
python -m app.main        # รันโค้ด Python
exit                      # ออกจาก container
```

#### 📊 ดู Logs
```bash
# ดู logs realtime
docker compose logs -f

# ดูเฉพาะ FastAPI
docker compose logs -f fastapi

# ดู 100 บรรทัดล่าสุด
docker compose logs --tail=100 fastapi
```

#### 🔄 Restart Services
```bash
# Restart เฉพาะ FastAPI
docker compose restart fastapi

# Restart ทั้งหมด
docker compose restart
```

#### 🧹 ทำความสะอาด
```bash
# หยุดและลบ containers
docker compose down

# ลบทั้ง containers และ volumes (ข้อมูลใน MySQL จะหายด้วย!)
docker compose down -v

# ลบ images ที่ไม่ใช้แล้ว
docker image prune
```

#### ⚡ Tips สำหรับการใช้ Docker อย่างเดียว

**ข้อดี:**
- ✅ ไม่ต้องติดตั้ง Python/uv เลย
- ✅ Environment เหมือน Production ทุกประการ
- ✅ ไม่มีปัญหา "works on my machine"

**ข้อเสีย:**
- ⚠️ ช้ากว่าการรันบนเครื่องโดยตรง
- ⚠️ IDE autocomplete อาจไม่ทำงาน
- ⚠️ Debug ยากกว่า

**เหมาะสำหรับ:**
- 🎯 คนที่ต้องการ setup ง่ายที่สุด
- 🎯 ทดสอบก่อน deploy
- 🎯 Demo ให้ทีม

---

### 2.4 ทดสอบว่า API ทำงาน

```bash
# ทดสอบ health check
curl http://localhost:8000/health

# เปิด API Documentation
# เบราว์เซอร์: http://localhost:8000/docs
```

---

## 3. โครงสร้าง Project

```
my-fastapi/
├── backend/                    # โฟลเดอร์หลักของ API
│   ├── app/                   # Application code
│   │   ├── __init__.py       # Package initialization
│   │   ├── main.py           # 🎯 Entry point - สร้าง FastAPI app
│   │   ├── config.py         # 🔧 Configuration & environment variables
│   │   ├── database.py       # 💾 Database connection & session management
│   │   │
│   │   ├── models/           # 📊 SQLAlchemy Database Models
│   │   │   ├── __init__.py
│   │   │   └── user.py       # User table definition
│   │   │
│   │   ├── schemas/          # 📋 Pydantic Schemas (Validation)
│   │   │   ├── __init__.py
│   │   │   └── user.py       # UserCreate, UserUpdate, UserResponse
│   │   │
│   │   ├── routers/          # 🛣️ API Endpoints (Routes)
│   │   │   ├── __init__.py
│   │   │   └── users.py      # User CRUD endpoints
│   │   │
│   │   └── utils/            # 🔨 Utility functions
│   │       ├── __init__.py
│   │       └── security.py   # Password hashing functions
│   │
│   ├── tests/                # 🧪 Unit tests
│   │   ├── __init__.py
│   │   ├── conftest.py       # Pytest fixtures
│   │   └── test_users.py     # User endpoint tests
│   │
│   ├── .env                  # 🔐 Environment variables (gitignored)
│   ├── .env.example          # 📄 Example environment variables
│   ├── pyproject.toml        # 📦 uv project configuration
│   ├── Dockerfile            # 🐳 Docker image definition
│   └── README.md             # 📖 Project documentation
│
├── docker-compose.yml        # 🐳 Multi-container setup (FastAPI + MySQL)
├── PLANNING.md              # 📐 Architecture decisions
├── TASK.md                  # ✅ Task tracking
├── CLAUDE.md                # 🤖 AI coding assistant rules
└── DEVELOPER_GUIDE.md       # 📘 This file!
```

### 3.1 ไฟล์สำคัญและหน้าที่

| ไฟล์ | หน้าที่ | เปิดดูบ่อยไหม |
|------|---------|---------------|
| `app/main.py` | สร้าง FastAPI app, register routers | ⭐⭐⭐ บ่อย |
| `app/routers/users.py` | API endpoints ทั้งหมดของ users | ⭐⭐⭐ บ่อยมาก |
| `app/models/user.py` | Database schema (ตาราง users) | ⭐⭐ ปานกลาง |
| `app/schemas/user.py` | Request/Response validation | ⭐⭐⭐ บ่อย |
| `app/database.py` | Database connection setup | ⭐ น้อย |
| `app/config.py` | Environment variables | ⭐ น้อย |
| `tests/test_users.py` | Unit tests | ⭐⭐⭐ บ่อย |

---

## 4. การไล่ Code: Request → Database → Response

### 4.1 ภาพรวม Request Flow

```
User Browser/Postman
        ↓
   [HTTP Request]
        ↓
FastAPI (app/main.py) ← Register routers here
        ↓
Router (app/routers/users.py) ← Handle endpoint
        ↓
Pydantic Schema (app/schemas/user.py) ← Validate input
        ↓
Database Session (app/database.py) ← Get DB connection
        ↓
SQLAlchemy Model (app/models/user.py) ← Query database
        ↓
MySQL Database
        ↓
   [Return data]
        ↓
Pydantic Schema ← Format response
        ↓
   [HTTP Response]
        ↓
User Browser/Postman
```

### 4.2 ตัวอย่าง: สร้าง User (POST /api/v1/users)

#### **Step 1: Request มาถึง FastAPI** (`app/main.py`)

```python
# app/main.py
from fastapi import FastAPI
from .routers import users_router

app = FastAPI(title="User Management API")

# Register router ที่จะจัดการ /api/v1/users/*
app.include_router(users_router)
```

#### **Step 2: Router รับ Request** (`app/routers/users.py`)

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(
    user: schemas.UserCreate,  # ← Pydantic จะ validate ให้อัตโนมัติ
    db: Session = Depends(get_db)  # ← Dependency injection: database session
):
    """Create a new user."""

    # Step 2.1: Check duplicate username/email
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.email)
    ).first()

    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=409, detail="Username already exists")
        raise HTTPException(status_code=409, detail="Email already exists")

    # Step 2.2: Hash password
    hashed_password = hash_password(user.password)

    # Step 2.3: Create user object
    db_user = models.User(
        **user.model_dump(exclude={"password"}),  # แปลง Pydantic → dict
        password_hash=hashed_password
    )

    # Step 2.4: Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Step 2.5: Return (Pydantic จะแปลงเป็น JSON ให้อัตโนมัติ)
    return db_user
```

#### **Step 3: Pydantic Validation** (`app/schemas/user.py`)

```python
# app/schemas/user.py - Request Schema
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # ← ตรวจสอบ email format
    password: str = Field(..., min_length=8)  # ← password ต้องยาวอย่างน้อย 8 ตัว
    full_name: Optional[str] = None
    role: str = Field(default="user", pattern="^(admin|user)$")

# app/schemas/user.py - Response Schema
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    # ← Pydantic v2: แปลง SQLAlchemy object → JSON
```

**สิ่งที่ Pydantic ช่วยเราทำ:**
- ✅ ตรวจสอบว่า username มีความยาว 3-50 ตัวอักษร
- ✅ ตรวจสอบว่า email เป็นรูปแบบที่ถูกต้อง
- ✅ ตรวจสอบว่า password ยาวอย่างน้อย 8 ตัว
- ✅ ตรวจสอบว่า role เป็น "admin" หรือ "user" เท่านั้น
- ✅ แปลง SQLAlchemy object → JSON response
- ❌ **ไม่ส่ง `password_hash` ใน response** (เพราะไม่ได้ประกาศใน UserResponse)

#### **Step 4: Database Query** (`app/models/user.py`)

```python
# app/models/user.py - SQLAlchemy Model
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    # ... fields อื่นๆ
```

**SQL ที่ถูก execute:**
```sql
-- Check duplicate
SELECT * FROM users
WHERE username = 'johndoe' OR email = 'john@example.com';

-- Insert new user
INSERT INTO users (username, email, password_hash, full_name, role, is_active)
VALUES ('johndoe', 'john@example.com', '$2b$12$...', 'John Doe', 'user', true);
```

#### **Step 5: Response** (JSON)

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2025-10-29T04:11:57",
  "updated_at": "2025-10-29T04:11:57"
}
```

**สังเกต:** `password` และ `password_hash` **ไม่ปรากฏ** ใน response เพื่อความปลอดภัย

### 4.3 ตัวอย่าง: List Users (GET /api/v1/users?skip=0&limit=10)

```python
# app/routers/users.py
@router.get("/", response_model=schemas.UserListResponse)
def list_users(
    skip: int = Query(default=0, ge=0),  # ← Query parameter validation
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    # Count total users
    total = db.query(models.User).count()

    # Get paginated users
    users = db.query(models.User).offset(skip).limit(limit).all()

    # Calculate page number
    page = (skip // limit) + 1 if limit > 0 else 1

    return {
        "users": users,
        "total": total,
        "page": page,
        "page_size": limit
    }
```

**SQL ที่ถูก execute:**
```sql
-- Count
SELECT COUNT(*) FROM users;

-- Get paginated data
SELECT * FROM users LIMIT 10 OFFSET 0;
```

---

## 5. การเข้าดูข้อมูลใน Database

### 5.1 วิธีที่ 1: ใช้ MySQL Command Line (ใน Docker Container)

```bash
# เข้าไปใน MySQL container
docker exec -it fastapi_mysql mysql -u fastapi_user -pfastapi_password user_management

# คำสั่ง SQL พื้นฐาน
mysql> SHOW TABLES;
mysql> DESCRIBE users;
mysql> SELECT * FROM users;
mysql> SELECT id, username, email, role FROM users;
mysql> SELECT * FROM users WHERE role = 'admin';
mysql> EXIT;
```

### 5.2 วิธีที่ 2: ใช้ MySQL Workbench

1. ดาวน์โหลด: https://dev.mysql.com/downloads/workbench/
2. สร้าง connection ใหม่:
   - **Hostname**: `localhost`
   - **Port**: `3306`
   - **Username**: `fastapi_user`
   - **Password**: `fastapi_password`
   - **Schema**: `user_management`
3. เชื่อมต่อและเขียน SQL queries

### 5.3 วิธีที่ 3: ใช้ DBeaver (แนะนำ - Free & Cross-platform)

1. ดาวน์โหลด: https://dbeaver.io/download/
2. สร้าง connection → MySQL
3. ใส่ข้อมูลเหมือนกับ MySQL Workbench
4. Browser tables และเขียน queries

### 5.4 วิธีที่ 4: ใช้ TablePlus (macOS - แนะนำสำหรับ Mac Users)

1. ดาวน์โหลด: https://tableplus.com/
2. สร้าง connection:
   - **Name**: User Management DB
   - **Host**: `localhost`
   - **Port**: `3306`
   - **User**: `fastapi_user`
   - **Password**: `fastapi_password`
   - **Database**: `user_management`

### 5.5 คำสั่ง SQL ที่ใช้บ่อย

```sql
-- ดูข้อมูลทั้งหมด
SELECT * FROM users;

-- ดูเฉพาะบาง columns
SELECT id, username, email, role, is_active FROM users;

-- Filter ข้อมูล
SELECT * FROM users WHERE role = 'admin';
SELECT * FROM users WHERE is_active = true;
SELECT * FROM users WHERE username LIKE '%john%';

-- Count
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM users WHERE role = 'admin';

-- Order by
SELECT * FROM users ORDER BY created_at DESC;
SELECT * FROM users ORDER BY username ASC;

-- ดู users ที่สร้างวันนี้
SELECT * FROM users WHERE DATE(created_at) = CURDATE();

-- ลบ user (ระวัง!)
DELETE FROM users WHERE id = 1;

-- Update user
UPDATE users SET full_name = 'New Name' WHERE id = 1;

-- ดู table structure
DESCRIBE users;
SHOW CREATE TABLE users;
```

---

## 6. การติดตั้ง Library Python เพิ่มเติม

### 6.1 การเพิ่ม Dependency ด้วย uv

```bash
# เข้าไปที่ backend folder
cd backend

# เพิ่ม production dependency
uv add <package-name>

# ตัวอย่าง: เพิ่ม requests library
uv add requests

# เพิ่ม dev dependency (เช่น testing, linting)
uv add --group dev <package-name>

# ตัวอย่าง: เพิ่ม black formatter
uv add --group dev black
```

**uv จะอัปเดต `pyproject.toml` อัตโนมัติ:**

```toml
# pyproject.toml
[project]
dependencies = [
    "fastapi>=0.104.0",
    "requests>=2.31.0",  # ← เพิ่มเข้ามาใหม่
]

[dependency-groups]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",  # ← เพิ่มเข้ามาใหม่
]
```

### 6.2 การใช้ Library ที่ติดตั้งแล้ว

**ตัวอย่าง: ใช้ requests เพื่อเรียก external API**

```python
# app/routers/users.py หรือไฟล์ใหม่
import requests

@router.get("/users/{user_id}/github")
def get_user_github_info(user_id: int, db: Session = Depends(get_db)):
    """Get user's GitHub information."""

    # Step 1: Get user from database
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 2: Call external API
    response = requests.get(f"https://api.github.com/users/{user.username}")

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="GitHub user not found")

    # Step 3: Return combined data
    return {
        "user": user,
        "github": response.json()
    }
```

### 6.3 การเพิ่ม Library สำหรับ Task ต่างๆ

```bash
# สำหรับเรียก external APIs
uv add httpx  # หรือ requests

# สำหรับ async tasks
uv add celery redis

# สำหรับ JWT authentication
uv add python-jose passlib

# สำหรับ file uploads
uv add python-multipart

# สำหรับ export Excel
uv add openpyxl pandas

# สำหรับ send emails
uv add fastapi-mail

# สำหรับ logging
uv add python-json-logger
```

### 6.4 การ Sync Dependencies (หลังจาก Pull Code จาก Git)

```bash
# ติดตั้ง dependencies ตาม pyproject.toml
uv sync

# หรือติดตั้งพร้อม dev dependencies
uv sync --group dev
```

---

## 7. การ Debug และดู Logs

### 7.1 ดู Logs จาก Docker

```bash
# ดู logs ทั้งหมด (realtime)
docker compose logs -f

# ดูเฉพาะ FastAPI logs
docker compose logs -f fastapi

# ดูเฉพาะ MySQL logs
docker compose logs -f mysql

# ดู logs ล่าสุด 100 บรรทัด
docker compose logs --tail=100

# ดู logs ของ specific container
docker logs fastapi_app -f
```

### 7.2 เพิ่ม Logging ในโค้ด

**การใช้ Python logging:**

```python
# app/routers/users.py
import logging

# สร้าง logger
logger = logging.getLogger(__name__)

@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Log เมื่อมี request เข้ามา
    logger.info(f"Creating user: {user.username}")

    # Check duplicate
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.email)
    ).first()

    if existing_user:
        logger.warning(f"Duplicate user attempt: {user.username}")
        raise HTTPException(status_code=409, detail="Username already exists")

    # Hash password
    hashed_password = hash_password(user.password)
    logger.debug(f"Password hashed for user: {user.username}")

    # Save to database
    db_user = models.User(
        **user.model_dump(exclude={"password"}),
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info(f"User created successfully: {user.username} (ID: {db_user.id})")
    return db_user
```

### 7.3 ดู Access Logs

**FastAPI + Uvicorn จะแสดง access logs อัตโนมัติ:**

```
INFO:     127.0.0.1:52301 - "POST /api/v1/users/ HTTP/1.1" 201 Created
INFO:     127.0.0.1:52302 - "GET /api/v1/users/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:52303 - "GET /api/v1/users/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52304 - "PUT /api/v1/users/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52305 - "DELETE /api/v1/users/1 HTTP/1.1" 204 No Content
```

**อ่าน Access Log:**
- `127.0.0.1:52301` - IP address และ port ของ client
- `POST /api/v1/users/` - HTTP method และ endpoint
- `201 Created` - HTTP status code

### 7.4 ดู Database Query Logs

**เปิด SQL query logging:**

```python
# app/database.py
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=True  # ← เปิดนี้เพื่อดู SQL queries
)
```

**Output ที่จะเห็น:**
```
INFO sqlalchemy.engine.Engine SELECT * FROM users WHERE id = ?
INFO sqlalchemy.engine.Engine [generated in 0.00023s] (1,)
INFO sqlalchemy.engine.Engine INSERT INTO users (username, email, ...) VALUES (?, ?, ...)
INFO sqlalchemy.engine.Engine [generated in 0.00045s] ('johndoe', 'john@example.com', ...)
```

### 7.5 Debug ด้วย Print Statements

**Debug ง่ายๆ ด้วย print:**

```python
@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(f"[DEBUG] Received user data: {user.model_dump()}")

    existing_user = db.query(models.User).filter(
        (models.User.username == user.username)
    ).first()

    print(f"[DEBUG] Existing user found: {existing_user is not None}")

    if existing_user:
        print(f"[DEBUG] Duplicate username: {user.username}")
        raise HTTPException(status_code=409, detail="Username already exists")

    # ... rest of code

    print(f"[DEBUG] User created with ID: {db_user.id}")
    return db_user
```

### 7.6 Debug ด้วย VS Code Debugger

**1. สร้างไฟล์ `.vscode/launch.json`:**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "jinja": true,
      "justMyCode": false,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

**2. วาง Breakpoints:**
- คลิกที่หมายเลขบรรทัดใน VS Code
- จุดสีแดงจะปรากฏ

**3. กด F5 เพื่อเริ่ม debug**

**4. เรียก API แล้วโปรแกรมจะหยุดที่ breakpoint**

### 7.7 ดู Error Stack Trace

**เมื่อเกิด error, FastAPI จะแสดง stack trace:**

```python
# ตัวอย่าง error
Traceback (most recent call last):
  File "app/routers/users.py", line 45, in create_user
    db_user = models.User(**user.model_dump())
  File "sqlalchemy/orm/decl_api.py", line 456, in __init__
    raise TypeError(f"Invalid argument: {key}")
TypeError: Invalid argument: password
```

**วิธีอ่าน:**
1. อ่านจากล่างขึ้นบน (บรรทัดล่างสุดคือสาเหตุจริง)
2. `TypeError: Invalid argument: password` - ปัญหาคือส่ง `password` ไปให้ Model แต่ Model ต้องการ `password_hash`
3. ดูที่ไฟล์และบรรทัดที่เกิด error: `app/routers/users.py", line 45`

---

## 🎯 Tips สำหรับ Junior Developers

### ✅ Do's:

1. **อ่าน logs อย่างสม่ำเสมอ** - จะช่วยให้เข้าใจ flow ของโปรแกรม
2. **ใช้ API docs** (`/docs`) - ทดสอบ endpoints ได้ง่ายกว่า Postman
3. **เขียน tests** - แก้ไขโค้ดได้ safe ขึ้น
4. **Commit บ่อยๆ** - ถ้าพัง revert ได้ง่าย
5. **อ่าน error messages อย่างละเอียด** - มักจะบอกสาเหตุชัดเจน

### ❌ Don'ts:

1. **อย่า commit `.env`** - มี secrets อยู่
2. **อย่าลืม `uv sync`** - หลัง pull code จาก git
3. **อย่าแก้ database โดยตรง** - ใช้ API หรือ migrations
4. **อย่าเปิด `echo=True` ใน production** - จะช้ามาก
5. **อย่า print sensitive data** - เช่น passwords, tokens

---

## 📚 Resources เพิ่มเติม

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Docker Documentation**: https://docs.docker.com/
- **Python Logging Tutorial**: https://docs.python.org/3/howto/logging.html

---

## ❓ คำถามที่พบบ่อย (FAQ)

**Q: ทำไม uv sync ไม่ work?**
A: ลอง `uv sync --reinstall` หรือลบ `.venv` แล้ว sync ใหม่

**Q: ทำไม Docker container หยุดเองทุกครั้ง?**
A: ดู logs ด้วย `docker compose logs` จะบอกสาเหตุ

**Q: ทำไม MySQL connection refused?**
A: รอให้ MySQL container พร้อมก่อน (ใช้เวลา 10-15 วินาที)

**Q: จะทดสอบ API ยังไง?**
A: ใช้ http://localhost:8000/docs (Swagger UI) หรือ Postman

**Q: จะดูว่า password ถูก hash หรือเปล่า?**
A: Query database แล้วดู `password_hash` column จะเห็น `$2b$12$...`

---

**Happy Coding! 🚀**

ถ้ามีคำถามเพิ่มเติม ถามได้เลยในทีม หรือเปิด issue ใน Git repository


---

## 📚 Table of Contents

- [Authentication & Authorization](#authentication--authorization)
  - [JWT Authentication Overview](#jwt-authentication-overview)
  - [Setup JWT Authentication](#setup-jwt-authentication)
  - [Using Authentication in Endpoints](#using-authentication-in-endpoints)
  - [Testing Authentication](#testing-authentication)
  - [Logout](#logout)

---

## Authentication & Authorization

### JWT Authentication Overview

โปรเจคนี้ใช้ **JWT (JSON Web Token)** สำหรับการ authentication แบบ stateless

**การทำงานของ JWT:**

```
1. User ส่ง username + password → /api/v1/auth/login
2. Server ตรวจสอบ credentials
3. ถ้าถูกต้อง → สร้าง JWT token และส่งกลับ
4. Client เก็บ token (localStorage/sessionStorage)
5. ทุกครั้งที่เรียก API → ส่ง token ใน Authorization header
6. Server ตรวจสอบ token และอนุญาตให้เข้าถึงข้อมูล
```

**ข้อดีของ JWT:**
- ✅ Stateless - Server ไม่ต้องเก็บ session
- ✅ Scalable - ใช้ได้กับ microservices
- ✅ Secure - มี signature ป้องกันการปลอมแปลง
- ✅ Self-contained - เก็บข้อมูล user ไว้ใน token

**ข้อเสียของ JWT:**
- ❌ ไม่สามารถ revoke token ได้ทันที (ต้องรอหมดอายุ)
- ❌ Token size ใหญ่กว่า session ID

---

### Setup JWT Authentication

#### 1. ติดตั้ง Dependencies

เพิ่มใน `pyproject.toml`:

```toml
[project]
dependencies = [
    "pyjwt>=2.8.0",
    # ... other dependencies
]
```

#### 2. เพิ่ม JWT Configuration

**ไฟล์: `.env`**
```env
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**คำแนะนำ:** สร้าง secret key ด้วยคำสั่ง:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**ไฟล์: `app/config.py`**
```python
class Settings(BaseSettings):
    # ... existing settings
    JWT_SECRET_KEY: str = "change-this-to-random-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

#### 3. สร้าง JWT Utilities

**ไฟล์: `app/utils/jwt.py`**
```python
"""JWT token utilities."""

from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status
from app.config import settings

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token.

    Args:
        data: Data to encode (usually {"sub": user_id, "username": username}).
        expires_delta: Token expiration time.

    Returns:
        Encoded JWT token string.
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
    """Verify and decode JWT token.

    Args:
        token: JWT token string.

    Returns:
        Decoded token payload.

    Raises:
        HTTPException: 401 if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

#### 4. สร้าง Login Endpoint

**ไฟล์: `app/schemas/auth.py`**
```python
"""Authentication schemas."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Login request schema."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
```

**ไฟล์: `app/routers/auth.py`**
```python
"""Authentication endpoints."""

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    db: Annotated[Session, Depends(get_db)]
) -> TokenResponse:
    """Login endpoint - authenticate user and return JWT token."""
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
```

#### 5. สร้าง Authentication Dependency

**ไฟล์: `app/dependencies/auth.py`**
```python
"""Authentication dependencies."""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.jwt import verify_access_token

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
```

**อธิบาย Dependency:**

`get_current_user` เป็น **Dependency Function** ที่:
1. FastAPI เรียกใช้อัตโนมัติก่อนเข้า endpoint
2. ดึง JWT token จาก Authorization header
3. ตรวจสอบความถูกต้องของ token
4. ค้นหา user จาก database
5. คืนค่า User object ให้กับ endpoint

**ถ้า token ไม่ถูกต้อง** → raise HTTPException 401 ทันที (endpoint ไม่ทำงาน)

---

### Using Authentication in Endpoints

#### ตัวอย่างการใช้งาน:

**ไฟล์: `app/routers/files.py`**
```python
from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/files", tags=["files"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)  # ← ต้อง authenticate
) -> dict:
    """Upload file (requires authentication)."""

    # ถ้าถึงบรรทัดนี้ = user login แล้ว
    # current_user = User object ของคนที่ login

    # ... upload logic ...

    return {
        "message": "File uploaded successfully",
        "uploaded_by": current_user.username  # ใช้ข้อมูล user ได้เลย
    }


@router.get("/")
async def list_files(
    current_user: User = Depends(get_current_user)  # ← ต้อง authenticate
) -> dict:
    """List files (requires authentication)."""
    # ... list logic ...
    return {"files": []}


@router.delete("/{filename}")
async def delete_file(
    filename: str,
    current_user: User = Depends(get_current_user)  # ← ต้อง authenticate
) -> dict:
    """Delete file (requires authentication)."""
    # ... delete logic ...
    return {"message": "Deleted", "deleted_by": current_user.username}
```

**หมายเหตุ:**
- เพิ่ม `current_user: User = Depends(get_current_user)` → endpoint ต้อง login
- ไม่เพิ่ม → ใครก็เรียกได้ (ไม่ต้อง login)

---

### Testing Authentication

#### 1. ทดสอบใน Swagger UI (http://localhost:8000/docs)

**Step 1: สร้าง User**
```
POST /api/v1/users/
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "role": "user"
}
```

**Step 2: Login**
```
POST /api/v1/auth/login
{
  "username": "testuser",
  "password": "password123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Step 3: Authorize**
1. กดปุ่ม **"Authorize"** (🔒) ที่มุมขวาบน
2. วาง token ลงในช่อง "Value" (ไม่ต้องใส่ "Bearer")
3. กด "Authorize"
4. กด "Close"

**Step 4: ทดสอบ Protected Endpoint**
```
POST /api/v1/files/upload
(เลือกไฟล์)

Response:
{
  "message": "File uploaded successfully",
  "uploaded_by": "testuser"
}
```

#### 2. ทดสอบด้วย cURL

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

**Upload file with token:**
```bash
curl -X POST http://localhost:8000/api/v1/files/upload \
  -H "Authorization: Bearer <your-token-here>" \
  -F "file=@/path/to/file.jpg"
```

#### 3. ทดสอบด้วย Python

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={"username": "testuser", "password": "password123"}
)
token = response.json()["access_token"]

# Upload file
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open("image.jpg", "rb")}
response = requests.post(
    "http://localhost:8000/api/v1/files/upload",
    headers=headers,
    files=files
)
print(response.json())
```

---

### Logout

JWT เป็น **stateless** ดังนั้น logout ทำที่ฝั่ง **client-side**:

#### วิธีการ Logout:

**JavaScript/React/Vue:**
```javascript
function logout() {
    // ลบ token จาก storage
    localStorage.removeItem('access_token');

    // Redirect ไปหน้า login
    window.location.href = '/login';
}
```

**Full Example:**
```javascript
// Login
async function login(username, password) {
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
}

// Use authenticated endpoint
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('access_token');

    const response = await fetch('http://localhost:8000/api/v1/files/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
    });

    return await response.json();
}

// Logout
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
}
```

**Swagger UI:**
1. กดปุ่ม "Authorize" (🔒)
2. กด "Logout"
3. กด "Close"

---

### Security Best Practices

1. **ใช้ HTTPS ใน production** - ป้องกัน token ถูกขโมย
2. **เก็บ secret key ปลอดภัย** - อย่า commit ลง git
3. **ตั้งเวลาหมดอายุสั้น** - เช่น 15-30 นาที
4. **ใช้ Refresh Token** - สำหรับขอ access token ใหม่
5. **Validate input ทุกครั้ง** - ป้องกัน injection attacks
6. **Log authentication events** - ติดตามการ login ที่ผิดปกติ

---

### Troubleshooting

**ปัญหา: 401 Unauthorized**
- ✅ ตรวจสอบว่า token ถูกต้อง
- ✅ ตรวจสอบว่า token ยังไม่หมดอายุ
- ✅ ตรวจสอบว่าใส่ "Bearer " นำหน้า token (มีช่องว่าง)
- ✅ ตรวจสอบว่า user ยังมีอยู่ใน database

**ปัญหา: Token หมดอายุเร็วเกินไป**
- เพิ่มค่า `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` ใน `.env`

**ปัญหา: Invalid token**
- ตรวจสอบว่า `JWT_SECRET_KEY` ตรงกันระหว่าง server instances

---

## Related Documentation

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - Decode and verify JWT tokens
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)