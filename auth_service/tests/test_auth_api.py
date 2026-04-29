import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_auth_flow(client: AsyncClient):
    # Register
    response = await client.post("/auth/register", json={"email": "test@email.com", "password": "testpass123"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@email.com"
    assert data["role"] == "user"

    # Login
    response = await client.post("/auth/login", data={"username": "test@email.com", "password": "testpass123"})
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # /me
    response = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    me_data = response.json()
    assert me_data["email"] == "test@email.com"


@pytest.mark.asyncio
async def test_register_conflict(client: AsyncClient):
    await client.post("/auth/register", json={"email": "dup@email.com", "password": "testpass123"})
    response = await client.post("/auth/register", json={"email": "dup@email.com", "password": "testpass123"})
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    await client.post("/auth/register", json={"email": "bad@email.com", "password": "testpass123"})
    response = await client.post("/auth/login", data={"username": "bad@email.com", "password": "wrongpass"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_without_token(client: AsyncClient):
    response = await client.get("/auth/me")
    assert response.status_code == 401