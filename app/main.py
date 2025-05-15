from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat, form, pdf, websocket
from .core.config import settings

app = FastAPI(title="AI Roadmap API")

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

@app.get("/")
async def root():
    return {"message": "AI Roadmap API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 