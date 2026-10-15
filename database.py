from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./recipes.db"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
