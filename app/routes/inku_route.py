import json
from fastapi import APIRouter, Depends, Request, Header, UploadFile, WebSocket, File
from sqlalchemy.orm import Session
from utils.deps import get_db
from sse_starlette import EventSourceResponse, ServerSentEvent
from service.inku_stream_service import ConnectionManager
from service.inkubator_service import InkubatorControlService
from service.image_procesing_service import ImageProccesingService
from service.sse_stream_service import SSEStreamService
from datetime import datetime
from schema import InkuTempRequest, StartIncubateRequest, AddDetailHatchRequest, UserInkuRequest
from typing import Annotated, Union
from PIL import Image
import os

routeInku = APIRouter()
    
# realtime server sent event


@routeInku.get('/sse/{user_id}/{token}')
async def message_stream_mobile(request: Request, user_id: str, token: str):
    return EventSourceResponse(
        SSEStreamService().event_generator_mobile(request, user_id, token),
        ping=60,
        ping_message_factory=lambda: ServerSentEvent(json.dumps({"ping": datetime.today().strftime('%Y-%m-%d %H:%M:%S')})))


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
async def post_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        datenow = datetime.now()
        filename = f"{str(datenow.date())}-{str(datenow.time())}-{file.filename}"

        file_path = os.path.join(path, filename)

        with open(file_path, "wb") as image_file:
            image_file.write(contents)

        return ImageProccesingService().EggCrackDetection(filename)
    except Exception as e:
        print(e)


@routeInku.post("/api/usr/start/inku")
def post_start_inkubating(request: StartIncubateRequest,  db: Session = Depends(get_db)):
    return InkubatorControlService().startIncubate(request, db)


@routeInku.post("/api/inku/report")
def post_report_inkubator(request: AddDetailHatchRequest, db: Session = Depends(get_db)):
    return InkubatorControlService.insertHatchDetail(request, db)


@routeInku.post("/api/inku/user")
def post_add_username_inku(request: UserInkuRequest, db: Session = Depends(get_db)):
    return InkubatorControlService.addUserInkubator(request, db)


@routeInku.get("/api/history/{textSearch}")
def get_history_search(textSearch: str, X_API_TOKEN: Annotated[Union[str, None], Header()] = None,  db: Session = Depends(get_db)):
    return InkubatorControlService.searchDataHistory(findTxt=textSearch, token=X_API_TOKEN, db=db)


@routeInku.get("/api/progress/{id_inkubator}")
def get_day_progress(id_inkubator: str, X_API_TOKEN: Annotated[Union[str, None], Header()] = None,  db: Session = Depends(get_db)):
    return InkubatorControlService.getDayProgress(X_API_TOKEN, id_inkubator, db)


@routeInku.get("/api/inku")
def getInkuUser(X_API_TOKEN: Annotated[Union[str, None], Header()] = None,  db: Session = Depends(get_db)):
    return InkubatorControlService.getInkubatorList(X_API_TOKEN, db)
