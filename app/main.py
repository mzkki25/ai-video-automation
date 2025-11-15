from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.video_routes import router as video_router
from app.api.auth_routes import router as auth_router
from app.api.history_routes import router as history_router
from app.api.template_routes import router as template_router
from app.api.page_routes import router as page_router
from app.api.upload_routes import router as upload_router
from app.api.avatar_routes import router as avatar_router
from app.core.Database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Video Automation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(page_router)
app.include_router(auth_router)
app.include_router(video_router)
app.include_router(history_router)
app.include_router(template_router)
app.include_router(upload_router)
app.include_router(avatar_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)