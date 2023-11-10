from app.database.dbConfig import SessionLocal 
from passlib.context import CryptContext

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")