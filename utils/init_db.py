# Only for local development or seeding

from app.database.get_db import init_db as real_init_db

async def init_db():
    await real_init_db()
