from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from model import models
from passlib.context import CryptContext


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

    def getPasswordContext(self):
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    def getPasswordHash(self, password):
        return self.getPasswordContext().hash(password)

    def verifyPassword(self, plainPassword, hasHPassword):
        return self.getPasswordContext().verify(plainPassword, hasHPassword)
