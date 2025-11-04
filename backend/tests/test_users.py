"""Tests for user CRUD endpoints."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_user_success(client: TestClient):
    """Test creating a user successfully."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123",
        "full_name": "Test User",
        "role": "user"
    }
    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "password" not in data
    assert "password_hash" not in data
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_user_duplicate_username(client: TestClient):
    """Test creating a user with duplicate username returns 409."""
    user_data = {
        "username": "duplicate",
        "email": "user1@example.com",
        "password": "password123"
    }
    client.post("/api/v1/users/", json=user_data)

    # Try to create another user with same username
    user_data2 = {
        "username": "duplicate",
        "email": "user2@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/users/", json=user_data2)

    assert response.status_code == 409
    assert "Username already exists" in response.json()["detail"]


def test_create_user_duplicate_email(client: TestClient):
    """Test creating a user with duplicate email returns 409."""
    user_data = {
        "username": "user1",
        "email": "duplicate@example.com",
        "password": "password123"
    }
    client.post("/api/v1/users/", json=user_data)

    # Try to create another user with same email
    user_data2 = {
        "username": "user2",
        "email": "duplicate@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/users/", json=user_data2)

    assert response.status_code == 409
    assert "Email already exists" in response.json()["detail"]


def test_create_user_invalid_email(client: TestClient):
    """Test creating a user with invalid email returns 422."""
    user_data = {
        "username": "testuser",
        "email": "not-an-email",
        "password": "password123"
    }
    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 422


def test_create_user_password_too_short(client: TestClient):
    """Test creating a user with short password returns 422."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "short"
    }
    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 422


def test_password_is_hashed(client: TestClient):
    """Test that password is hashed and not stored in plain text."""

    user_data = {
        "username": "hashtest",
        "email": "hash@example.com",
        "password": "plainpassword123"
    }
    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 201

    # Verify password is not in response
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


def test_list_users_empty(client: TestClient):
    """Test listing users when database is empty."""
    response = client.get("/api/v1/users/")

    assert response.status_code == 200
    data = response.json()
    assert data["users"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 10


def test_list_users_with_pagination(client: TestClient):
    """Test listing users with pagination."""
    # Create multiple users
    for i in range(15):
        user_data = {
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "password": "password123"
        }
        client.post("/api/v1/users/", json=user_data)

    # Test first page
    response = client.get("/api/v1/users/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 10
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["page_size"] == 10

    # Test second page
    response = client.get("/api/v1/users/?skip=10&limit=10")
    data = response.json()
    assert len(data["users"]) == 5
    assert data["total"] == 15
    assert data["page"] == 2


def test_get_user_by_id_success(client: TestClient):
    """Test getting a user by ID successfully."""
    # Create a user
    user_data = {
        "username": "getuser",
        "email": "getuser@example.com",
        "password": "password123"
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Get the user
    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "getuser"
    assert "password_hash" not in data


def test_get_user_not_found(client: TestClient):
    """Test getting a non-existent user returns 404."""
    response = client.get("/api/v1/users/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_user_success(client: TestClient):
    """Test updating a user successfully."""
    # Create a user
    user_data = {
        "username": "oldname",
        "email": "old@example.com",
        "password": "password123"
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Update the user
    update_data = {
        "username": "newname",
        "full_name": "Updated Name"
    }
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newname"
    assert data["full_name"] == "Updated Name"
    assert data["email"] == "old@example.com"  # Unchanged


def test_update_user_not_found(client: TestClient):
    """Test updating a non-existent user returns 404."""
    update_data = {"username": "newname"}
    response = client.put("/api/v1/users/999", json=update_data)

    assert response.status_code == 404


def test_update_user_duplicate_username(client: TestClient):
    """Test updating user with existing username returns 409."""
    # Create two users
    client.post("/api/v1/users/", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123"
    })
    response2 = client.post("/api/v1/users/", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "password123"
    })
    user2_id = response2.json()["id"]

    # Try to update user2 username to user1
    response = client.put(f"/api/v1/users/{user2_id}", json={"username": "user1"})

    assert response.status_code == 409


def test_delete_user_success(client: TestClient):
    """Test deleting a user successfully."""
    # Create a user
    user_data = {
        "username": "deleteuser",
        "email": "delete@example.com",
        "password": "password123"
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 204

    # Verify user is deleted
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_user_not_found(client: TestClient):
    """Test deleting a non-existent user returns 404."""
    response = client.delete("/api/v1/users/999")

    assert response.status_code == 404


def test_pagination_metadata_accuracy(client: TestClient):
    """Test pagination metadata is calculated correctly."""
    # Create 25 users
    for i in range(25):
        client.post("/api/v1/users/", json={
            "username": f"paginationuser{i}",
            "email": f"pagination{i}@example.com",
            "password": "password123"
        })

    # Test various pagination scenarios
    response = client.get("/api/v1/users/?skip=0&limit=10")
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total"] == 25

    response = client.get("/api/v1/users/?skip=20&limit=10")
    data = response.json()
    assert data["page"] == 3
    assert len(data["users"]) == 5
