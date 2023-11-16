from app.database.dbConfig import Base
from sqlalchemy import String, Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
import sys

sys.path.append("..")


class UserModel(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, unique=True, index=True)
    password = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    token = Column(String(100))

    inkubators = relationship("InkubatorsModel", back_populates="user")

    # def __repr__(self):
    #     return {
    #         "username ": self.username,
    #         "name" : self.name
    #     }


class InkubatorsModel(Base):
    __tablename__ = "inkubators"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(10), index=True)
    temp_limit = Column(Integer)
    humd_limit = Column(Integer)
    water_volume = Column(Integer)
    temp_value = Column(Integer)
    humd_value = Column(Integer)
    username = Column(String(100), ForeignKey("users.username"))

    user = relationship("UserModel", back_populates="inkubators")
    hatch_data = relationship("HatchDataModel", back_populates="inkubator")


class HatchDataModel(Base):
    __tablename__ = "hatch_data"

    id = Column(Integer, primary_key=True, index=True)
    inkubator_id = Column(Integer, ForeignKey(
        "inkubators.id"))  # Foreign key relationship
    start_date = Column(Date)
    end_date_estimation = Column(Date)
    number_of_eggs = Column(Integer)

    inkubator = relationship("InkubatorsModel", back_populates="hatch_data")
    detail_hatch = relationship("DetailHatchDataModel", back_populates="hatch_data")

class DetailHatchDataModel(Base):
    __tablename__ = "detail_hatch_data"

    id = Column(Integer, primary_key=True, index=True)
    id_hatch_data = Column(Integer, ForeignKey("hatch_data.id"))
    temp = Column(Integer)
    humd = Column(Integer)
    water_volume = Column(Integer)
    time = Column(String),
    date_report = Column(Date)

    hatch_data = relationship("HatchDataModel", back_populates="detail_hatch_data")
