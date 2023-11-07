from sqlalchemy import Column, String, Integer, DATE
from database import Base


class HatchDataModel(Base):
    __tablename__ = "hatch_data"

    id  = Column(Integer, primary_key=True, index=True)
    inkubator_id = Column(Integer, nullable=False)
    start_data = Column(DATE)
    end_data_estimation = Column(DATE)
    number_of_egg = Column(Integer)