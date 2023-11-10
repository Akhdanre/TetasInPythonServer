from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import sys

sys.path.append("..")
from app.model import models


class ValidationService:
    def validation(username, db: Session):
        
        try:
            user_db = db.query(models.UserModel).filter_by(
                username=username).first()
            if user_db:
                return True
            return False
        except SQLAlchemyError as e:
            return False
