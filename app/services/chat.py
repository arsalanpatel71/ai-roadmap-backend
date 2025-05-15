from openai import AsyncOpenAI
from ..core.config import settings
from ..schemas.chat import ChatMessage
import asyncio
import os
from ..services.form import get_user_request

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class ChatService:
    def __init__(self):
        self.threads = {} 
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.assistant_id = settings.ASSISTANT_ID

    async def get_or_create_thread(self, user_id: str):
        if user_id not in self.threads:
            thread = await client.beta.threads.create()
            self.threads[user_id] = thread.id
        return self.threads[user_id]

    async def get_chat_response(self, request_id: str, message: str) -> str:
        user_data = await get_user_request(request_id)
        
        system_context = f"""
        You are an AI Roadmap Assistant. You have the following information about the user:
        - Company: {user_data['form']['company_name']}
        - Industry: {user_data['form']['industry']}
        - Company Size: {user_data['form']['company_size']}
        - Job Title: {user_data['form']['job_title']}

        Use this information to provide personalized recommendations. Do not ask for information that was already provided in the form.
        Focus on understanding their specific AI needs and challenges based on their industry and company size.
        """

        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": message}
            ]
        )
        
        return response.choices[0].message.content

chat_service = ChatService()

async def get_chat_response(messages: list[ChatMessage]) -> str:
    """Legacy function for compatibility with existing code"""
    if not messages:
        return ""
    last_message = messages[-1]
    temp_user_id = "temp_" + os.urandom(4).hex()
    return await chat_service.get_chat_response(temp_user_id, last_message.content) 