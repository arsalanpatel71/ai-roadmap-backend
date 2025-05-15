from ..core.database import db
from ..schemas.form import UserRequest, FormData
from datetime import datetime
from bson import ObjectId

async def create_user_request(form_data: FormData) -> str:
    user_request = UserRequest(
        form=form_data,
        created_at=datetime.utcnow()
    )
    result = await db.users.insert_one(user_request.model_dump())
    return str(result.inserted_id)

async def update_chat_history(request_id: str, message: dict):
    await db.users.update_one(
        {"_id": ObjectId(request_id)},
        {"$push": {"chat_history": message}}
    )

async def update_pdf_info(request_id: str, pdf_info: dict):
    await db.users.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"pdf": pdf_info}}
    )

async def get_user_request(request_id: str):
    return await db.users.find_one({"_id": ObjectId(request_id)})

async def save_form_data(form_data: FormData) -> str:
    result = await db.forms.insert_one(form_data.model_dump())
    return str(result.inserted_id)

async def get_form_data(form_id: str):
    form = await db.forms.find_one({"_id": ObjectId(form_id)})
    return form 