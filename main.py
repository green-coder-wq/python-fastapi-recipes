from typing import AsyncGenerator, List, cast

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import CursorResult, select, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from database import Base, async_session, engine

app = FastAPI(
    title="Кулинарная книга",
    description="API сервиса рецептов.",
    version="1.0.0",
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await engine.dispose()


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeListItem],
    tags=["Рецепты"],
    summary="Список всех рецептов",
    description=(
        "Рецепты отсортированы по убыванию просмотров, "
        "при равенстве — по возрастанию времени приготовления."
    ),
)
async def list_recipes(
    session: AsyncSession = Depends(get_session),
) -> List[models.Recipe]:
    result = await session.execute(
        select(models.Recipe).order_by(
            models.Recipe.views.desc(),
            models.Recipe.cooking_time.asc(),
        )
    )
    return list(result.scalars().all())


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeDetail,
    tags=["Рецепты"],
    summary="Детальная информация о рецепте",
    description="Возвращает рецепт и увеличивает счётчик просмотров на 1.",
    responses={404: {"description": "Рецепт с таким id не найден"}},
)
async def get_recipe(
    recipe_id: int,
    session: AsyncSession = Depends(get_session),
) -> models.Recipe:
    update_result = cast(
        CursorResult,
        await session.execute(
            update(models.Recipe)
            .where(models.Recipe.id == recipe_id)
            .values(views=models.Recipe.views + 1)
        ),
    )
    if update_result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    await session.commit()

    select_result = await session.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    return select_result.scalar_one()


@app.post(
    "/recipes",
    response_model=schemas.RecipeDetail,
    status_code=201,
    tags=["Рецепты"],
    summary="Создать новый рецепт",
)
async def create_recipe(
    payload: schemas.RecipeIn,
    session: AsyncSession = Depends(get_session),
) -> models.Recipe:
    recipe = models.Recipe(
        title=payload.title,
        cooking_time=payload.cooking_time,
        description=payload.description,
        views=0,
    )
    recipe.ingredients = [
        models.Ingredient(
            name=ing.name,
            amount=ing.amount,
            unit=ing.unit,
        )
        for ing in payload.ingredients
    ]

    session.add(recipe)
    await session.commit()
    await session.refresh(recipe)
    return recipe
