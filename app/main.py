from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat, form, pdf, websocket
from .core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(form.router, prefix="/api/form", tags=["form"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(pdf.router, prefix="/api/pdf", tags=["pdf"])
app.include_router(websocket.router, tags=["websocket"]) 
