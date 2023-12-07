from fastapi import APIRouter, Depends, Request, Header, File, UploadFile, WebSocket
from sqlalchemy.orm import Session
from app.utils.deps import get_db
from sse_starlette import EventSourceResponse, ServerSentEvent
from app.service.inku_stream_service import ConnectionManager
from app.service.inkubator_service import InkubatorControlService
from app.service.image_procesing_service import ImageProccesingService
from datetime import datetime
from app.schema import InkuTempRequest, StartIncubateRequest, AddDetailHatchRequest, UserInkuRequest
from typing import Annotated, Union
from PIL import Image
import json

routeInku = APIRouter()

# realtime server sent event


# @routeInku.get('/sse/control/{inku_id}/{token}')
# async def message_stream(request: Request, inku_id: int, token: str):
#     return EventSourceResponse(
#         InkuStreamService().event_generator_inku(request, inku_id, token),
#         ping=60,
#         ping_message_factory=lambda: ServerSentEvent({"ping": datetime.today().strftime('%Y-%m-%d %H:%M:%S')}))


# @routeInku.get('/sse/info/hatch')
# async def message_stream(request: Request, user_id: str, token: str):
#     return EventSourceResponse(
#         InkuStreamService().event_generator_mobile(request, user_id, token),
#         ping=60,
#         ping_message_factory=lambda: ServerSentEvent({"ping": datetime.today().strftime('%Y-%m-%d %H:%M:%S')}))


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


path = "assets/image"


@routeInku.post("/api/inku/image")
async def post_image(file: UploadFile):
    contents = await file.read()
    file_path = f"{path}/{file.filename}"

    with open(file_path, "wb") as image_file:
        image_file.write(contents)

    return ImageProccesingService().EggCrackDetection(file.filename)


@routeInku.post("/api/usr/start/inku")
def post_start_inkubating(request: StartIncubateRequest,  db: Session = Depends(get_db)):
    return InkubatorControlService().startIncubate(request, db)


@routeInku.post("/api/inku/report")
def post_report_inkubator(request: AddDetailHatchRequest, db: Session = Depends(get_db)):
    return InkubatorControlService.insertHatchDetail(request, db)


@routeInku.post("/api/inku/user")
def post_add_username_inku(request: UserInkuRequest, db: Session = Depends(get_db)):
    return InkubatorControlService.addUserInkubator(request, db)


# WebSocket
manager = ConnectionManager()


@routeInku.websocket("/ws/control")
async def Websocket_endpoint(websocket: WebSocket, db:  Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.on_message(data, websocket, db)
    except Exception as e:
        print("Got an exception ", e)
        await manager.disconnect(websocket)
