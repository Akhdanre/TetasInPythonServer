import sys

sys.path.append("..")
from app.database.dbConfig import SessionLocal 

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()