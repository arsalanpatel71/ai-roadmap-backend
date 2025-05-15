from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class CompanySize(str, Enum):
    SMALL = "1-10"
    MEDIUM = "11-50"
    LARGE = "51-200"
    ENTERPRISE = "200+"

class FormData(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    company_name: str
    industry: str
    company_size: CompanySize
    job_title: str

class ChatMessage(BaseModel):
    role: str
    message: str
    timestamp: datetime = datetime.utcnow()

class PDFInfo(BaseModel):
    filename: str
    path: str
    generated_at: datetime = datetime.utcnow()

class UserRequest(BaseModel):
    form: FormData
    chat_history: List[ChatMessage] = []
    pdf: Optional[PDFInfo] = None
    created_at: datetime = datetime.utcnow()

class UserResponse(BaseModel):
    request_id: str
    message: str 