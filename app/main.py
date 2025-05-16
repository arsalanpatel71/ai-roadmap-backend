from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat, form, pdf, websocket
from .core.config import settings
from .core.database import db_manager
from .core import clients
import httpx

app = FastAPI(title="AI Roadmap API")

@app.on_event("startup")
async def startup_event():
    print("Application startup...")
    await db_manager.connect_db()
    clients.http_client = httpx.AsyncClient()
    clients.openai_client = clients.AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY,
        http_client=clients.http_client
    )
    print("Database and OpenAI client initialized.")

@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutdown...")
    await db_manager.close_db()
    if clients.http_client:
        await clients.http_client.aclose()
    print("Database and HTTP client closed.")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(form.router, prefix="/api/form", tags=["form"])
app.include_router(pdf.router, prefix="/api/pdf", tags=["pdf"])
app.include_router(websocket.router, prefix="/api/ws", tags=["websocket"])

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "AI Roadmap API is running"}

@app.get("/health", tags=["Health Check"])
async def health_check():
    try:
        if db_manager.client:
            await db_manager.client.admin.command('ping')
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {"status": "healthy", "database": db_status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 