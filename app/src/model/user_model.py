from sqlalchemy import String, Column
from database import Base


class UserModel(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, unique=True, index=True)
    password = Column(String(100), index=True)
    name = Column(String(100), index=True)
    token = Column(String(100), index=True)

