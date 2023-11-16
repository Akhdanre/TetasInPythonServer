from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from app.model import UserModel, InkubatorsModel, HatchDataModel, client_data, DetailHatchDataModel
from app.schema import InkuTempRequest
from fastapi import HTTPException, status
import json
from app.utils import WebResponseData, ExceptionCustom


class InkubatorControlService:
    def __init__(self):
        self.RETRY_TIMEOUT = 15000

    def inkuControlTempHumd(self, request: InkuTempRequest, db: Session):
        try:
            inkubator = db.query(InkubatorsModel).filter_by(
                id=request.target_id).first()
            if inkubator:
                inkubator.temp_limit = request.temp_limit
                inkubator.humd_limit = request.humd_limit
                db.commit()
                db.refresh(inkubator)
                new_message = {
                    "retry": self.RETRY_TIMEOUT,
                    "data": {
                        "temp": inkubator.temp_limit,
                        "humd": inkubator.humd_limit
                    }
                }
                if str(request.target_id) in client_data.connected_inku_client:
                    inkubator_data = client_data.connected_inku_client[str(
                        request.target_id)]
                    inkubator_data[1].put_nowait(new_message)
                    return WebResponseData(data="ok")
                else:
                    return WebResponseData(errors=f"Inkubator with id {request.target_id} not online", code=status.HTTP_400_BAD_REQUEST)

                # this condition is for all change inkubator control

                # if request.condition is False and (len(client_data.connected_inku_client) > 0):
                #     for data in client_data.connected_inku_client.values():
                #         data[1].put_nowait(new_message)
                #     return JSONResponse({"data": "ok"})
                # return JSONResponse({"data": "something odd"}, 400)

            return WebResponseData(errors="inkubaotors not found", code=status.HTTP_400_BAD_REQUEST)
        except SQLAlchemyError as e:
            raise ExceptionCustom(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def getInfoInku(token_request: str, db: Session):
        try:
            inkubator = db.query(InkubatorsModel).filter_by(
                token=token_request).first()
            if inkubator:
                return WebResponseData(data={
                    "temp": inkubator.temp_value,
                    "humd": inkubator.humd_value,
                    "water_level": inkubator.water_volume
                })
            return WebResponseData(errors="inkubaotors not found", code=status.HTTP_400_BAD_REQUEST)
        except SQLAlchemyError as e:
            raise ExceptionCustom(
                status_code=400, detail=str(e))

    def hatch_data_to_dict(self, hatch_data):
        return [
            {
                'id': entry.id,
                'inkubator_id': entry.inkubator_id,
                'start_data': entry.start_date.isoformat() if entry.start_date else None,
                'end_data_estimation': entry.end_date_estimation.isoformat() if entry.end_date_estimation else None,
                'number_of_egg': entry.number_of_eggs,
            }
            for entry in hatch_data
        ]

    def getDataReport(self, header_token: str, db: Session):
        try:
            # First, find the user based on the provided token
            user = db.query(UserModel).filter_by(token=header_token).first()

            if user:
                # If the user is found, get the hatch data associated with the user
                hatch_data = db.query(HatchDataModel).join(InkubatorsModel).filter(
                    InkubatorsModel.username == user.username
                ).order_by(desc(HatchDataModel.id)).all()
                data_result = self.hatch_data_to_dict(hatch_data)
                # Now, 'hatch_data' contains a list of HatchDataModel objects associated with the user
                return WebResponseData(data=data_result)
            else:
                # Handle the case where the user with the provided token is not found
                return WebResponseData(errors="data None", code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle exceptions as needed
            print(f"Error retrieving data: {e}")
            return None

    def getDetailReport(id: int, token: str, db: Session):
        try:
            data = db.query(DetailHatchDataModel).filter_by(
                id_hatch_data=id).all()
            if data:
                listData = [
                    {
                        "id": entry.id,
                        "id_hatch_data": entry.id_hatch_data,
                        "temp": entry.temp,
                        "humd": entry.humd,
                        "water_volume": entry.water_volume,
                        "time": entry.time_report,
                        "date": str(entry.date_report)
                    } for entry in data
                ]
                return WebResponseData(listData)
            return WebResponseData(errors="data None", code=400)
        except SQLAlchemyError as e:
            print(e)
            return None
