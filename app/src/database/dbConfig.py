from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:oukenzeumasio@localhost:3306/testFastApi"

engine = create_engine(  
SQLALCHEMY_DATABASE_URL, 
connect_args={"check_same_thread": False}  
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def session_scope() -> SessionLocal:
    db = None
    try:
        db = SessionLocal()  
        yield db
    finally:
        db.close()
