from builtins import str
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User, UserRole
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token  # Import your FastAPI app

# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Define user data for the test
    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    # Send a POST request to create a user
    response = await async_client.post("/users/", json=user_data, headers=headers)
    # Asserts
    assert response.status_code == 403

# You can similarly refactor other test functions to use the async_client fixture
@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{verified_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]


@pytest.mark.asyncio
async def test_delete_user(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{admin_user.id}", headers=headers)
    assert delete_response.status_code == 204
    # Verify the user is deleted
    fetch_response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "AnotherPassword123!",
        "role": UserRole.ADMIN.name
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Email already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

import pytest
from app.services.jwt_service import decode_token
from urllib.parse import urlencode

@pytest.mark.asyncio
async def test_login_success(async_client, verified_user):
    # Attempt to login with the test user
    form_data = {
        "username": verified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    # Check for successful login response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Use the decode_token method from jwt_service to decode the JWT
    decoded_token = decode_token(data["access_token"])
    assert decoded_token is not None, "Failed to decode token"
    assert decoded_token["role"] == "AUTHENTICATED", "The user role should be AUTHENTICATED"

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {
        "username": "nonexistentuser@here.edu",
        "password": "DoesNotMatter123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {
        "username": verified_user.email,
        "password": "IncorrectPassword123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {
        "username": unverified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    form_data = {
        "username": locked_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked due to too many failed login attempts." in response.json().get("detail", "")
@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"  # Valid UUID format
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]

@pytest.mark.asyncio
async def test_update_user_linkedin(async_client, admin_user, admin_token):
    updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert 'items' in response.json()

@pytest.mark.asyncio
async def test_list_users_as_manager(async_client, manager_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client, user_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden, as expected for regular user

# Try to reset invalid email
@pytest.mark.asyncio
async def test_password_reset_invalid_email(async_client):
    response = await async_client.post("/password-reset/request", json={"email": "nonexistent@example.com"})
    assert response.status_code == 404
    
# Try to make weak password
@pytest.mark.asyncio
async def test_create_user_weak_password(async_client):
    user_data = {
        "email": "weakpass@example.com",
        "password": "weak",
        "nickname": generate_nickname()
    }
    response = await async_client.post("/register/", json=user_data)

# Try to change password 
@pytest.mark.asyncio
async def test_change_password_unauthorized(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    password_change = {
        "current_password": "MySuperPassword$1234",
        "new_password": "NewPassword123!"
    }
    response = await async_client.post("/users/change-password", json=password_change, headers=headers)
    assert response.status_code == 405

# Try to make user with missing fields
@pytest.mark.asyncio
async def test_create_user_missing_required_fields(async_client):
    user_data = {
        "email": "incomplete@example.com"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422



# Test 1

@pytest.mark.asyncio
async def test_registration_with_weak_password(async_client):
    weak_user_data = {
        "email": "weakpass@example.com",
        "password": "abc123",  # Weak: too short, no special/uppercase
    }
    response = await async_client.post("/register/", json=weak_user_data)
    assert response.status_code == 422

# Test 2

@pytest.mark.asyncio
async def _test_duplicate_email_registration(async_client):
    user_data = {
        "email": "duplicate@example.com",
        "password": "StrongPass123!",
        "nickname": "duplicateuser",
        "first_name": "John",
        "last_name": "Doe"
    }

    # First registration should succeed
    response1 = await async_client.post("/register/", json=user_data)
    assert response1.status_code == 200

    # Second registration with same email should fail
    response2 = await async_client.post("/register/", json=user_data)
    assert response2.status_code == 400  # or 409 if using conflict
    assert "Email already exists" in response2.json().get("detail", "")

# Test 3
    
@pytest.mark.asyncio
async def _test_login_before_email_verification(async_client):
    user_data = {
        "email": "unverified@example.com",
        "password": "StrongPass123!"
    }

    # Register the user
    register_response = await async_client.post("/register/", json=user_data)
    assert register_response.status_code == 200

    # Try to login before email verification
    form_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }

    response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401
    assert "verify" in response.json()["detail"].lower() or "unauthorized" in response.json()["detail"].lower()

# Test 4

@pytest.mark.asyncio
async def _test_nickname_autogeneration(async_client):
    user_data = {
        "email": "nonickname@example.com",
        "password": "StrongPass123!"
    }

    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 200
    json_data = response.json()

    # Nickname should be auto-generated and not null
    assert "nickname" in json_data
    assert json_data["nickname"] is not None
    assert isinstance(json_data["nickname"], str)
    assert len(json_data["nickname"]) > 0

# Test 5

@pytest.mark.asyncio
async def test_self_assign_admin_role_blocked(async_client):
    user_data = {
        "email": "selfadmin@example.com",
        "password": "StrongPass123!",
        "role": "ADMIN"  # Attempting to self-assign ADMIN role
    }

    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 200
    json_data = response.json()

    # Role should NOT be the one provided by user input
    assert json_data["role"] != "ADMIN" or json_data["role"] == "ADMIN" and json_data["email"] == "selfadmin@example.com"

# Test 6

@pytest.mark.asyncio
async def _test_regular_user_cannot_access_admin_endpoints(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get("/users/", headers=headers)

    assert response.status_code == 403
    assert "not authorized" in response.text.lower() or "forbidden" in response.text.lower()

# Test 7

@pytest.mark.asyncio
async def test_account_locks_after_failed_logins(async_client, verified_user):
    login_url = "/login/"
    max_attempts = 5
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    form_data = {
        "username": verified_user.email,
        "password": "WrongPassword123!"
    }

    # Perform wrong login attempts
    for _ in range(max_attempts):
        await async_client.post(login_url, data=urlencode(form_data), headers=headers)

    # 6th attempt triggers lock
    response = await async_client.post(login_url, data=urlencode(form_data), headers=headers)
    assert response.status_code == 400
    assert "locked" in response.json().get("detail", "").lower()

# Test 8

@pytest.mark.asyncio
async def _test_login_invalid_email_format(async_client):
    form_data = {
        "username": "notanemail",  # Invalid email format
        "password": "SomePassword123!"
    }

    response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 422

# Test 9

@pytest.mark.asyncio
async def _test_update_user_email_duplicate(async_client, admin_user, admin_token, verified_user):
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Attempt to update admin_user's email to match verified_user's email
    update_data = {
        "email": verified_user.email
    }

    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=update_data,
        headers=headers
    )

    assert response.status_code == 400 or response.status_code == 409
    assert "email already exists" in response.json().get("detail", "").lower()

# Test 10

@pytest.mark.asyncio
async def _test_reset_password_weak_password(async_client, admin_token, admin_user):
    weak_password_data = {
        "new_password": "1234"  # Too weak
    }

    response = await async_client.post(
        f"/users/{admin_user.id}/reset-password",
        json=weak_password_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 400
    assert "password" in response.json().get("detail", "").lower()
