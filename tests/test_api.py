import pytest


@pytest.mark.asyncio
async def test_create_recipe(client):
    payload = {
        "title": "Борщ",
        "cooking_time": 90,
        "description": "Классический рецепт борща",
        "ingredients": [
            {"name": "Свёкла", "amount": 2, "unit": "шт"},
            {"name": "Капуста", "amount": 300, "unit": "г"},
        ],
    }
    response = await client.post("/recipes", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Борщ"
    assert data["views"] == 0
    assert len(data["ingredients"]) == 2


@pytest.mark.asyncio
async def test_get_recipes_empty(client):
    response = await client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_recipe_by_id(client):
    payload = {
        "title": "Пельмени",
        "cooking_time": 60,
        "description": "Домашние пельмени",
        "ingredients": [
            {"name": "Мясо", "amount": 500, "unit": "г"},
        ],
    }
    created = (await client.post("/recipes", json=payload)).json()

    response = await client.get(f"/recipes/{created['id']}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == created["id"]
    assert data["title"] == "Пельмени"
    assert data["views"] == 1


@pytest.mark.asyncio
async def test_get_recipe_not_found(client):
    response = await client.get("/recipes/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_views_increment(client):
    payload = {
        "title": "Окрошка",
        "cooking_time": 30,
        "description": "Летний суп",
        "ingredients": [
            {"name": "Кефир", "amount": 1, "unit": "л"},
        ],
    }
    created = (await client.post("/recipes", json=payload)).json()

    await client.get(f"/recipes/{created['id']}")
    await client.get(f"/recipes/{created['id']}")

    response = await client.get(f"/recipes/{created['id']}")
    assert response.json()["views"] == 3


@pytest.mark.asyncio
async def test_create_recipe_empty_title(client):
    payload = {
        "title": "",
        "cooking_time": 30,
        "description": "Без названия",
        "ingredients": [
            {"name": "Вода", "amount": 1, "unit": "л"},
        ],
    }
    response = await client.post("/recipes", json=payload)
    assert response.status_code == 422
