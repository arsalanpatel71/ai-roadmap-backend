from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import List, Dict
import json
from ..services.chat import chat_service  
from ..schemas.chat import ChatMessage
from ..schemas.pdf import PDFRequest
from ..services.pdf import generate_pdf
import os
from ..core.database import db
from ..schemas.form import UserRequest, FormData
from datetime import datetime
from ..services.form import get_user_request, update_chat_history  
from bson.errors import InvalidId
from bson import ObjectId
import uuid

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {} 
        
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            
    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{request_id}")
async def websocket_endpoint(websocket: WebSocket, request_id: str):
    try:
        try:
            ObjectId(request_id)
        except InvalidId:
            await websocket.close(code=4000, reason="Invalid request ID format")
            return

        user_data = await get_user_request(request_id)
        if not user_data:
            await websocket.close(code=4004, reason="Request not found")
            return

        await manager.connect(websocket, request_id)
        
        welcome_message = (
            f"I have reviewed your details. Please confirm if this information is correct:\n\n"
            f"Name: {user_data['form']['first_name']} {user_data['form']['last_name']}\n"
            f"Company: {user_data['form']['company_name']}\n"
            f"Industry: {user_data['form']['industry']}\n"
            f"Company Size: {user_data['form']['company_size']}\n"
            f"Job Title: {user_data['form']['job_title']}\n\n"
            f"Is this information correct? Once confirmed, we can proceed with creating your AI roadmap."
        )
        
        ai_message = {
            "role": "assistant",
            "message": welcome_message,
            "timestamp": datetime.utcnow()
        }
        await update_chat_history(request_id, ai_message)
        await manager.send_personal_message(
            json.dumps({
                "sender": "assistant",
                "message": welcome_message
            }),
            request_id
        )
        
        try:
            while True:
                data = await websocket.receive_text()
                
                message = {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "message": data,
                    "timestamp": datetime.utcnow()
                }
                await update_chat_history(request_id, message)
                
                try:
                    ai_response = await chat_service.get_chat_response(request_id, data)
                    
                    ai_message = {
                        "id": str(uuid.uuid4()),
                        "role": "assistant",
                        "message": ai_response,
                        "timestamp": datetime.utcnow()
                    }
                    await update_chat_history(request_id, ai_message)
                    
                    await manager.send_personal_message(
                        json.dumps({
                            "id": ai_message["id"],
                            "sender": "assistant",
                            "message": ai_response
                        }),
                        request_id
                    )

                    if "phase" in ai_response.lower() and any(phase in ai_response.lower() for phase in ["phase 1", "phase 2", "phase 3", "phase 4"]):
                        user_data = await get_user_request(request_id)
                        
                        formatted_content = ai_response.replace("\n", "<br>")
                        formatted_content = formatted_content.replace("###", "<h3>").replace("\n\n", "</h3>")
                        
                        pdf_request = PDFRequest(
                            template_name="ai_roadmap",
                            data={
                                "title": f"AI Implementation Roadmap for {user_data['form']['company_name']}",
                                "company_name": user_data['form']['company_name'],
                                "industry": user_data['form']['industry'],
                                "company_size": user_data['form']['company_size'],
                                "content": formatted_content
                            },
                            output_filename=f"roadmap_{user_data['form']['company_name'].lower().replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
                        )
                        
                        pdf_path = await generate_pdf(pdf_request)
                        
                        pdf_info = {
                            "filename": os.path.basename(pdf_path),
                            "path": pdf_path,
                            "generated_at": datetime.utcnow()
                        }
                        await update_pdf_info(request_id, pdf_info)
                        
                        await manager.send_personal_message(
                            json.dumps({
                                "sender": "system",
                                "message": "Your AI Roadmap PDF has been generated!",
                                "pdf_url": f"/pdf/download/{os.path.basename(pdf_path)}"
                            }),
                            request_id
                        )

                        await manager.send_personal_message(
                            json.dumps({
                                "sender": "assistant",
                                "message": ai_response
                            }),
                            request_id
                        )

                except Exception as e:
                    await manager.send_personal_message(
                        json.dumps({
                            "sender": "system",
                            "message": f"Error: {str(e)}"
                        }),
                        request_id
                    )
                
        except WebSocketDisconnect:
            manager.disconnect(request_id)
        except Exception as e:
            await manager.send_personal_message(
                json.dumps({
                    "sender": "system",
                    "message": f"Error: {str(e)}"
                }),
                request_id
            )
            
    except Exception as e:
        if not websocket.client_state.DISCONNECTED:
            await websocket.close(code=4000, reason=str(e)) 