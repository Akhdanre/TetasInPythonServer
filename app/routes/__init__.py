from fastapi import APIRouter
from .user_route import router

api_router = APIRouter()

api_router.include_router(router)