from ..core.config import settings
from ..schemas.chat import ChatMessage
from ..core import clients
from ..services.form import get_user_request

class ChatService:
    def __init__(self):
        self.threads = {}
        self.assistant_id = settings.ASSISTANT_ID
        if not self.assistant_id:
            print("Warning: ASSISTANT_ID is not set in settings.")

    async def get_or_create_thread(self, user_id: str):
        if not clients.openai_client:
            raise RuntimeError("OpenAI client not initialized. Check application startup.")
        if user_id not in self.threads:
            thread = await clients.openai_client.beta.threads.create()
            self.threads[user_id] = thread.id
        return self.threads[user_id]

    async def get_chat_response(self, request_id: str, message: str) -> str:
        if not clients.openai_client:
            raise RuntimeError("OpenAI client not initialized. Check application startup.")
            
        user_data = await get_user_request(request_id)
        if not user_data or 'form' not in user_data:
            print(f"Warning: User data or form not found for request_id: {request_id}")
            return "Error: Could not retrieve user information to personalize the chat."

        company_name = user_data['form'].get('company_name', 'N/A')
        industry = user_data['form'].get('industry', 'N/A')
        company_size = user_data['form'].get('company_size', 'N/A')
        job_title = user_data['form'].get('job_title', 'N/A')

        system_context = f"""
        You are an AI Roadmap Assistant. You have the following information about the user:
        - Company: {company_name}
        - Industry: {industry}
        - Company Size: {company_size}
        - Job Title: {job_title}

        Use this information to provide personalized recommendations. Do not ask for information that was already provided in the form.
        Focus on understanding their specific AI needs and challenges based on their industry and company size.
        """

        response = await clients.openai_client.chat.completions.create(
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