from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime
import uuid

class ChatMessage(BaseModel):
    id: str = str(uuid.uuid4())
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = datetime.utcnow()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str
    
class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    
class ChatResponse(BaseModel):
    response: str
    thread_id: Optional[str] = None 