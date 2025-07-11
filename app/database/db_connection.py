"""
Database connection and session management for async SQLAlchemy.
Loads DB credentials from .env.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = BASE_DIR / '.env'

load_dotenv(dotenv_path=dotenv_path)

POSTGRES_URL = f"postgresql+asyncpg://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_async_engine(POSTGRES_URL, echo=True)

async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_session():
    """Yield an async database session for dependency injection."""
    async with async_session_maker() as session:
        yield session


