from fastapi import APIRouter
from sse_starlette import EventSourceResponse
from app.service.inku_stream_service import InkuStreamService


routeInku = APIRouter()



@routeInku.get("/sse/control/temp")
async def temp_stream():
    return EventSourceResponse(InkuStreamService.event_generator())



