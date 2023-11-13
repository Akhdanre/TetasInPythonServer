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
            inkubator = db.query(models.InkubatorsModel).filter_by(
                id=request.target_id).first()
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
                    print("data", client_data.connected_inku_client)
                    if str(request.target_id) in client_data.connected_inku_client:
                        inkubator_data = client_data.connected_inku_client[str(
                            request.target_id)]
                        inkubator_data[1].put_nowait(new_message)
                        return JSONResponse({"data": "ok"})
                    else:
                        print(
                            f"Inkubator with id {request.target_id} not online")
                        return JSONResponse({"data": "inkubator not online"}, 400)
                if request.condition is False and (len(client_data.connected_inku_client) > 0):
                    for data in client_data.connected_inku_client.values():
                        data[1].put_nowait(new_message)
                    return JSONResponse({"data": "ok"})
                return JSONResponse({"data": "something odd"})

            print(f"data : {inkubator.id}")
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
