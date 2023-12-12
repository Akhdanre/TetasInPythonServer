from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc, or_, func
from app.model import UserModel, InkubatorsModel, HatchDataModel, client_data, DetailHatchDataModel
from app.schema import InkuTempRequest, StartIncubateRequest, AddDetailHatchRequest, UserInkuRequest
from fastapi import status
from app.utils import WebResponseData, ExceptionCustom
from datetime import datetime, timedelta


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
            user = db.query(UserModel).filter_by(token=header_token).first()

            if user:
                hatch_data = db.query(HatchDataModel).join(InkubatorsModel).filter(
                    InkubatorsModel.username == user.username
                ).order_by(desc(HatchDataModel.id)).all()
                data_result = self.hatch_data_to_dict(hatch_data)
                return WebResponseData(data=data_result)
            else:
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

    def startIncubate(self, data: StartIncubateRequest,  db: Session):
        tanggal_string = data.start_date
        array_tanggal = tanggal_string.split('-')
        tahun = int(array_tanggal[0])
        bulan = int(array_tanggal[1])
        tanggal = int(array_tanggal[2])

        tanggal_awal = datetime(tahun, bulan, tanggal)
        tanggal_kedepan = tanggal_awal + timedelta(days=7)
        try:
            insert = HatchDataModel(
                inkubator_id=data.id_inkubator,
                start_date=data.start_date,
                end_date_estimation=tanggal_kedepan.strftime('%Y-%m-%d'),
                number_of_eggs=data.number_of_egg
            )
            db.add(insert)
            db.commit()
            db.refresh(insert)
            new_message = {
                "retry": self.RETRY_TIMEOUT,
                "data": {
                    "id": insert.id
                }
            }
            if str(data.id_inkubator) in client_data.connected_inku_client:
                inkubator_data = client_data.connected_inku_client[str(
                    data.id_inkubator)]
                inkubator_data[1].put_nowait(new_message)
                return WebResponseData(data="ok")
            else:
                return WebResponseData(errors=f"Inkubator with id {data.id_inkubator} not online", code=status.HTTP_400_BAD_REQUEST)
        except SQLAlchemyError as e:
            print(e)
            return None

    def insertHatchDetail(request: AddDetailHatchRequest, db: Session):
        try:
            insert = DetailHatchDataModel(
                id_hatch_data=request.id_hatch_data,
                temp=request.temp,
                humd=request.humd,
                water_volume=request.water_volume,
                time_report=datetime.now().strftime('%H:%M:%S'),
                date_report=datetime.now().strftime('%Y-%m-%d')
            )
            db.add(insert)
            db.commit()
            db.refresh(insert)
            return WebResponseData(data="ok")
        except SQLAlchemyError as e:
            print(e)
            return None

    def addUserInkubator(request: UserInkuRequest, db: Session):
        try:
            update = db.query(InkubatorsModel).filter_by(
                id=request.id, token=request.token).first()
            if update:
                update.username = request.username
                db.commit()
                db.refresh(update)
                return WebResponseData(data="ok")
            return WebResponseData(errors="inkubator not found", code=404)
        except SQLAlchemyError as e:
            print(e)
            return None

    def searchDataHistory(token: str, findTxt: str, db: Session):
        try:
            data = db.query(HatchDataModel) \
                .filter(
                    or_(
                        HatchDataModel.inkubator_id.ilike(f"%{findTxt}%"),
                        HatchDataModel.start_date.ilike(f"%{findTxt}%"),
                        HatchDataModel.end_date_estimation.ilike(f"%{findTxt}%"))) \
                .all()
            if data:
                dataItem = [HatchDataModel.to_dict()
                            for HatchDataModel in data]
                print(dataItem)
                return WebResponseData(data=dataItem)
            return WebResponseData(errors="data not found", code=404)
        except SQLAlchemyError as e:
            print(f"error : {e}")
            return WebResponseData(errors="something wrong", code=500)

    def getDayProgress(token: str, inkubator_id: int, db: Session):
        try:

            result = db.query(func.count(func.distinct(DetailHatchDataModel.date_report)))\
                .filter_by(id_hatch_data=inkubator_id)\
                .scalar()

            if result:
                return WebResponseData(data=result)
            return WebResponseData(errors="progress not found", code=204)
        except SQLAlchemyError as e:
            print(f"error : {e}")
            return WebResponseData(errors="something wrong", code=500)
