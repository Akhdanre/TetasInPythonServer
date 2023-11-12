from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.model import models
from app.schema import InkuTempRequest


class InkubatorControlService:

    def tempControl(request: InkuTempRequest, db: Session):
        try:
            inkubator = db.query(
                models.InkubatorsModel).filter_by(id=id).first()
            if inkubator:
                inkubator.min_temp = InkuTempRequest.min_temp
                inkubator.max_temp = InkuTempRequest.max_temp

                db.commit()
                db.refresh(inkubator)
                return None
            return None
        except SQLAlchemyError as e:
            raise

    def humdControl():
        return None

    def status():
        return None


   