import asyncio
import logging
from sqlalchemy import text
from app.database import engine

logger = logging.getLogger("keep_alive")

async def keep_alive_db_worker(interval_seconds: int = 300):
    """
    Background worker that runs a simple 'SELECT 1' query on the database
    at regular intervals (default: 5 minutes) to keep connections active
    and prevent cloud databases (e.g. Supabase) from going to sleep.
    """
    logger.info(f"Database keep-alive worker started (pinging every {interval_seconds}s)...")
    while True:
        try:
            await asyncio.sleep(interval_seconds)
            # Execute simple ping query in a non-blocking thread
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, _ping_database)
            logger.info("Database keep-alive ping successful.")
        except asyncio.CancelledError:
            logger.info("Database keep-alive worker stopped.")
            break
        except Exception as e:
            logger.error(f"Database keep-alive ping failed: {e}")

def _ping_database():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

