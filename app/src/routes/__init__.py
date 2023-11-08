from fastapi import APIRouter
from . import user_controller

api_router = APIRouter()

api_router.include_router(user_controller.router)