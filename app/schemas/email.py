from pydantic import BaseModel, EmailStr
from typing import List, Optional

class EmailSchema(BaseModel):
    email_to: List[EmailStr]
    subject: str
    body: str
    attachments: Optional[List[str]] = None 