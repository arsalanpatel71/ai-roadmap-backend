from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client.aryng_db 