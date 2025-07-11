# Optional: DB init (for dev use only)

"""
Database initialization script for local development.
Use to create all tables defined in SQLAlchemy models.
"""

from app.models import Base
from app.database.db_connection import engine

async def init_db():
    """Create all database tables asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)