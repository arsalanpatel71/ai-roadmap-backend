from fastapi import APIRouter, HTTPException
from ..schemas.form import FormData, UserResponse
from ..services.form import create_user_request

router = APIRouter()

@router.post("/submit", response_model=UserResponse)
async def submit_form(form_data: FormData):
    try:
        request_id = await create_user_request(form_data)
        
        return UserResponse(
            request_id=request_id,
            message="Form submitted successfully. Please connect to the chat to continue."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 