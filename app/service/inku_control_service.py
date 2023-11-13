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

    def inkuControlTempHumd(self, request: InkuTempRequest, db: Session):
        try:
            inkubator = db.query(models.InkubatorsModel).filter_by(
                id=request.target_id).first()
            if inkubator:
                inkubator.temp_limit = request.temp_limit
                inkubator.humd_limit = request.humd_limit
                db.commit()
                db.refresh(inkubator)
                new_message = {
                    "retry": self.RETRY_TIMEOUT,
                    "data": {
                        "temp": request.temp_limit,
                        "humd": request.humd_limit
                    }
                }
                if str(request.target_id) in client_data.connected_inku_client:
                    inkubator_data = client_data.connected_inku_client[str(
                        request.target_id)]
                    inkubator_data[1].put_nowait(new_message)
                    return JSONResponse({"data": "ok"})
                else:
                    return JSONResponse({"data": f"Inkubator with id {request.target_id} not online"}, 400)

                # this condition is for all change inkubator control

                # if request.condition is False and (len(client_data.connected_inku_client) > 0):
                #     for data in client_data.connected_inku_client.values():
                #         data[1].put_nowait(new_message)
                #     return JSONResponse({"data": "ok"})
                # return JSONResponse({"data": "something odd"}, 400)

            raise HTTPException(400, detail="inkubator not found")
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e
            )

    def getInfoInku(token_request: str, db: Session):
        try:
            inkubator = db.query(models.InkubatorsModel).filter_by(
                token=token_request).first()
            if inkubator:
                return JSONResponse({"data": {
                    "temp": inkubator.temp_limit,
                    "humd": inkubator.humd_limit,
                    "water_level": inkubator.water_volume
                }})
            return JSONResponse({"data": "inkubator doesn't exist"}, 400)
        except SQLAlchemyError as e:
            return JSONResponse({"data": e}, 400)
