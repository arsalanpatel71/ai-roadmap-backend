from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings
import logging
import asyncio # Not strictly needed here anymore with class methods
from typing import Optional

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db = None # This will hold the database instance, e.g., client.roadmap

    @classmethod
    async def connect_db(cls):
        if cls.client is None: # Connect only if not already connected
            try:
                logger.info(f"Attempting to connect to MongoDB URI: {settings.MONGO_URI[:20]}...") # Log partial URI for security
                cls.client = AsyncIOMotorClient(settings.MONGO_URI)
                # Replace 'roadmap' with your actual database name if different
                cls.db = cls.client.roadmap 
                
                # Test the connection
                await cls.client.admin.command('ping')
                logger.info("Successfully connected to MongoDB and selected database.")
                
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {str(e)}")
                # Depending on your app's needs, you might want to exit or handle this gracefully
                raise
        else:
            logger.info("MongoDB connection already established.")


    @classmethod
    async def close_db(cls):
        if cls.client:
            await cls.client.close()
            cls.client = None # Reset client
            cls.db = None # Reset db instance
            logger.info("Closed MongoDB connection.")

    @classmethod
    def get_db_instance(cls): # Renamed for clarity
        if cls.db is None:
            # This case should ideally be handled by ensuring connect_db is called at startup
            logger.warning("get_db_instance called before database was initialized or after it was closed.")
            # raise RuntimeError("Database not initialized. Call connect_db first.")
        return cls.db

# Single instance of the Database class to manage state
db_manager = Database()

async def get_database():
    # This function ensures connection for dependency injection if needed,
    # but primary connection is handled at startup.
    if not db_manager.client or not db_manager.db:
        await db_manager.connect_db()
    return db_manager.get_db_instance() 