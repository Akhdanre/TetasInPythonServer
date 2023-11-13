from fastapi import APIRouter


from .user_route import router
from .auth_route import route
from .inku_route import routeInku

api_router = APIRouter()

api_router.include_router(router)
api_router.include_router(route)
api_router.include_router(routeInku)
