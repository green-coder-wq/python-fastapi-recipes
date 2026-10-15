from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    cooking_time = Column(Integer, nullable=False)
    views = Column(Integer, default=0, nullable=False)
    description = Column(Text, nullable=False)

    ingredients = relationship(
        "Ingredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    unit = Column(String, nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")
