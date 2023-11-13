from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse, ServerSentEvent
from app.service.inku_stream_service import InkuStreamService
from datetime import datetime


routeInku = APIRouter()

@routeInku.get('/sse/control/temp/{user_id}/{token}')
async def message_stream(request: Request, user_id: str, token: str):

    return EventSourceResponse(
        InkuStreamService.event_generator(request, user_id, token),
        ping=60,
        ping_message_factory=lambda: ServerSentEvent({"ping": datetime.today().strftime('%Y-%m-%d %H:%M:%S')}))
