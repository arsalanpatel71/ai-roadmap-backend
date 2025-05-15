from fastapi import APIRouter, HTTPException
from ..schemas.chat import ChatMessage, ChatResponse
from ..services.chat import chat_service
import os

router = APIRouter()

@router.post("/send", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    try:
        temp_user_id = "temp_" + os.urandom(4).hex()
        response = await chat_service.get_chat_response(temp_user_id, message.content)
        return ChatResponse(message=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 