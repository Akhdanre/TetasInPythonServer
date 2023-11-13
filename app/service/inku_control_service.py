from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.model import models
from app.model import client_data
from app.schema import InkuTempRequest
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status


class InkubatorControlService:
    def __init__(self):
        self.RETRY_TIMEOUT = 15000

    def tempControl(self, request: InkuTempRequest, db: Session):
        try:
            print(request.target_id, request.target_token)
            inkubator = db.query(
                models.InkubatorsModel).filter_by(id=request.target_id).first()
            if inkubator:
                inkubator.min_temp = request.min_temp
                inkubator.max_temp = request.max_temp
                db.commit()
                db.refresh(inkubator)
                new_message = {
                    "event": "new_message",
                    "id": "message_id",
                    "retry": self.RETRY_TIMEOUT,
                    "data": {
                        "max": request.max_temp,
                        "min": request.min_temp
                    }
                }
                if request.condition:
                    if request.target_id in client_data.connected_inku_client:
                        client_data.connected_inku_client[request.target_id][1].put_nowait(
                            new_message)
                        return JSONResponse({"data": "ok"})
                    return JSONResponse({"data": "inkubator doesn't exist"}, 400)
                if (len(client_data.connected_inku_client) > 0):
                    for client_id, data in client_data.connected_inku_client.items():
                        data[1].put_nowait(new_message)
                    return JSONResponse({"data": "ok"})
            raise HTTPException(400, detail="inkubator not found")
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e
            )

    def humdControl():
        return None

    def status():
        return None
