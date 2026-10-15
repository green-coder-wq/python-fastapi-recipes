import pytest
from httpx import AsyncClient, Response

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Create async test client fixture."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root(client: AsyncClient) -> None:
    """Test root endpoint."""
    response: Response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """Test health check endpoint."""
    response: Response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient) -> None:
    """Test creating a new item."""
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 9.99,
    }
    response: Response = await client.post("/items/", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 9.99
    assert "id" in data


@pytest.mark.asyncio
async def test_get_items(client: AsyncClient) -> None:
    """Test getting all items."""
    response: Response = await client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient) -> None:
    """Test getting non-existent item."""
    response: Response = await client.get("/items/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
