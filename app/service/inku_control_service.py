from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.model import models
from app.schema import InkuTempRequest
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status


class InkubatorControlService:
    def __init__(self):
        self.RETRY_TIMEOUT = 15000

    def tempControl(self, request: InkuTempRequest, db: Session):
        try:
            inkubator = db.query(
                models.InkubatorsModel).filter_by(id=id).first()
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
                if data.condition:
                    models.connected_clients[data.target_id][1].put_nowait(
                        new_message)
                    return JSONResponse({"data": "ok"})

                for client_id, data in models.connected_clients.items():
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
