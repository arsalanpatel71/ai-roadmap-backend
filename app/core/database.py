from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

try:
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client.roadmap  # Use your database name
    
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
    
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    # Provide a fallback or raise an appropriate error
    raise

def get_database():
    return db 