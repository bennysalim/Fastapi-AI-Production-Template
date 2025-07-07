import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from typing import AsyncGenerator

load_dotenv()

# Async engine
engine: AsyncEngine = create_async_engine(os.getenv("DB_URL"), echo=True)

# Session factory
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# Async DB init
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)