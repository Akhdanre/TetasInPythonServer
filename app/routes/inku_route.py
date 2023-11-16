from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session
from app.utils.deps import get_db
from sse_starlette import EventSourceResponse, ServerSentEvent
from app.service.inku_stream_service import InkuStreamService
from app.service.inkubator_service import InkubatorControlService
from datetime import datetime
from app.schema import InkuTempRequest
from typing import Annotated, Union

routeInku = APIRouter()

# realtime server sent event

@routeInku.get('/sse/control/temp/{user_id}/{token}')
async def message_stream(request: Request, user_id: str, token: str):
    return EventSourceResponse(
        InkuStreamService().event_generator(request, user_id, token),
        ping=60,
        ping_message_factory=lambda: ServerSentEvent({"ping": datetime.today().strftime('%Y-%m-%d %H:%M:%S')}))

@routeInku.get('/sse/info/hatch')
async def message_stream(request: Request, user_id: str, token: str):
    return EventSourceResponse(
        InkuStreamService().event_generator_mobile(request, user_id, token),
        ping=60,
        ping_message_factory=lambda: ServerSentEvent({"ping": datetime.today().strftime('%Y-%m-%d %H:%M:%S')}))


# http method
@routeInku.post("/api/control/temp_humd")
def message_data(data: InkuTempRequest, db: Session = Depends(get_db)):
    return InkubatorControlService().inkuControlTempHumd(request=data, db=db)


@routeInku.get("/api/inku/info/{token}")
def get_info(token: str, db: Session = Depends(get_db)):
    return InkubatorControlService.getInfoInku(token, db)


@routeInku.get("/api/data/report")
def get_data_report(X_API_TOKEN: Annotated[Union[str, None], Header()] = None, db: Session = Depends(get_db)):
    return InkubatorControlService().getDataReport(X_API_TOKEN, db)


@routeInku.get("/api/data/report/detail/{id_data}")
def get_data_report(id_data: int, X_API_TOKEN: Annotated[Union[str, None], Header()] = None, db: Session = Depends(get_db)):
    return InkubatorControlService.getDetailReport(id_data, X_API_TOKEN, db)
