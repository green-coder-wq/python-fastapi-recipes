from typing import List

from pydantic import BaseModel, ConfigDict, Field


class IngredientIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Название ингредиента",
        examples=["Свёкла"],
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Количество",
        examples=[2],
    )
    unit: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Единица измерения",
        examples=["шт"],
    )


class IngredientOut(IngredientIn):
    id: int = Field(..., description="Идентификатор ингредиента")

    model_config = ConfigDict(orm_mode=True, str_strip_whitespace=True)


class RecipeIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Название рецепта",
        examples=["Борщ"],
    )
    cooking_time: int = Field(
        ...,
        gt=0,
        description="Время приготовления в минутах",
        examples=[90],
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Текстовое описание приготовления",
    )
    ingredients: List[IngredientIn] = Field(
        ...,
        min_length=1,
        description="Список ингредиентов",
    )


class RecipeListItem(BaseModel):
    """Для первого экрана — таблица со списком."""

    id: int = Field(..., description="Идентификатор рецепта")
    title: str = Field(..., description="Название рецепта")
    views: int = Field(..., description="Сколько раз открывали детальную страницу")
    cooking_time: int = Field(..., description="Время приготовления в минутах")

    model_config = ConfigDict(orm_mode=True)


class RecipeDetail(BaseModel):
    """Для второго экрана — детальная информация."""

    id: int = Field(..., description="Идентификатор рецепта")
    title: str = Field(..., description="Название рецепта")
    cooking_time: int = Field(..., description="Время приготовления в минутах")
    views: int = Field(..., description="Сколько раз открывали детальную страницу")
    description: str = Field(..., description="Текстовое описание приготовления")
    ingredients: List[IngredientOut] = Field(..., description="Список ингредиентов")

    model_config = ConfigDict(orm_mode=True)
