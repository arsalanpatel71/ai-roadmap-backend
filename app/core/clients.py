from openai import AsyncOpenAI
import httpx
from typing import Optional

# These will be initialized in main.py's startup event
http_client: Optional[httpx.AsyncClient] = None
openai_client: Optional[AsyncOpenAI] = None 