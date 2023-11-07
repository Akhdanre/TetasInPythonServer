from sqlalchemy import Column, String, Integer
from database import Base
class InkubatorsModel(Base):
    __tablename__ = "inkubators"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(10), index=True)
    min_temp = Column(Integer(2))
    max_temp = Column(Integer(2))
    min_humd = Column(Integer(2))
    max_humd = Column(Integer(2))
    water_volume = Column(Integer(2))
    username = Column(String(100))