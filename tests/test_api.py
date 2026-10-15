import pytest
from httpx import AsyncClient, Response


@pytest.mark.asyncio
async def test_create_recipe(client: AsyncClient) -> None:
    payload = {
        "title": "Борщ",
        "cooking_time": 90,
        "description": "Классический рецепт борща",
        "ingredients": [
            {"name": "Свёкла", "amount": 2, "unit": "шт"},
            {"name": "Капуста", "amount": 300, "unit": "г"},
        ],
    }
    response: Response = await client.post("/recipes", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Борщ"
    assert data["views"] == 0
    assert len(data["ingredients"]) == 2


@pytest.mark.asyncio
async def test_get_recipes_empty(client: AsyncClient) -> None:
    response: Response = await client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_recipe_by_id(client: AsyncClient) -> None:
    payload = {
        "title": "Пельмени",
        "cooking_time": 60,
        "description": "Домашние пельмени",
        "ingredients": [
            {"name": "Мясо", "amount": 500, "unit": "г"},
        ],
    }
    created: Response = await client.post("/recipes", json=payload)
    created_data = created.json()

    response: Response = await client.get(f"/recipes/{created_data['id']}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == created_data["id"]
    assert data["title"] == "Пельмени"
    assert data["views"] == 1


@pytest.mark.asyncio
async def test_get_recipe_not_found(client: AsyncClient) -> None:
    response: Response = await client.get("/recipes/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_views_increment(client: AsyncClient) -> None:
    payload = {
        "title": "Окрошка",
        "cooking_time": 30,
        "description": "Летний суп",
        "ingredients": [
            {"name": "Кефир", "amount": 1, "unit": "л"},
        ],
    }
    created: Response = await client.post("/recipes", json=payload)
    created_data = created.json()

    await client.get(f"/recipes/{created_data['id']}")
    await client.get(f"/recipes/{created_data['id']}")

    response: Response = await client.get(f"/recipes/{created_data['id']}")
    assert response.json()["views"] == 3


@pytest.mark.asyncio
async def test_create_recipe_empty_title(client: AsyncClient) -> None:
    payload = {
        "title": "",
        "cooking_time": 30,
        "description": "Без названия",
        "ingredients": [
            {"name": "Вода", "amount": 1, "unit": "л"},
        ],
    }
    response: Response = await client.post("/recipes", json=payload)
    assert response.status_code == 422
