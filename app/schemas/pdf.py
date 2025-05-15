from pydantic import BaseModel
from typing import Dict, Any, Optional

class PDFRequest(BaseModel):
    template_name: str
    data: Dict[str, Any]
    output_filename: Optional[str] = None

class PDFResponse(BaseModel):
    file_path: str
    message: str 