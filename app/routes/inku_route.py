from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.utils.deps import get_db
from sse_starlette import EventSourceResponse, ServerSentEvent
from app.service.inku_stream_service import InkuStreamService
from app.service.inku_control_service import InkubatorControlService
from datetime import datetime
from app.schema import InkuTempRequest

routeInku = APIRouter()


@routeInku.get('/sse/control/temp/{user_id}/{token}')
async def message_stream(request: Request, user_id: str, token: str):

    return EventSourceResponse(
        InkuStreamService.event_generator(request, user_id, token),
        ping=60,
        ping_message_factory=lambda: ServerSentEvent({"ping": datetime.today().strftime('%Y-%m-%d %H:%M:%S')}))


@routeInku.post("/data")
def message_data(data: InkuTempRequest, db: Session = Depends(get_db)):
    return InkubatorControlService.tempControl(data, db)
