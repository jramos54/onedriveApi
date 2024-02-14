from fastapi import FastAPI
from .routers import router

app = FastAPI(title="OneDrive API",
    description="API para subir documentos de server a OneDrive",
    version="1.0.0",
    docs_url="/docs",  
    redoc_url="/redoc",
    debug=True  
)

app.include_router(router)
