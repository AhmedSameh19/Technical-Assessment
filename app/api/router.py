from fastapi import APIRouter

from app.api.machines import router as machines_router

api_router = APIRouter()
api_router.include_router(machines_router)
