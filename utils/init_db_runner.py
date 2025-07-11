"""
Command-line runner to initialize the database schema for development.
"""

import asyncio
from utils.init_db import init_db

if __name__ == "__main__":
    asyncio.run(init_db())
