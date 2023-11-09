from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:oukenzeumasio@localhost:3306/tetasin_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def session_scope() -> SessionLocal:
    db = None
    try:
        print("is session")
        db = SessionLocal()
        yield db
    finally:
        db.close()
