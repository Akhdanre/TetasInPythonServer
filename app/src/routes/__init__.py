from fastapi import APIRouter
from . import user_route

api_router = APIRouter()

api_router.include_router(user_route.router)