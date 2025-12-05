from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="AI Energy Manager API",
    description="Backend API for AI Energy Manager with Anomaly Detection and AI Chat",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import chat, dashboard, machines

app.include_router(chat.router)
app.include_router(dashboard.router)
app.include_router(machines.router)

@app.get("/")
async def root():
    return {"message": "AI Energy Manager API is running"}
