from sqlalchemy import String, Column, Integer, Date
from database.dbConfig import Base


class UserModel(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, unique=True, index=True)
    password = Column(String(100), index=True)
    name = Column(String(100), index=True)
    token = Column(String(100), index=True)
    
    def __repr__(self):
        return f"UserModel('{self.username}', '{self.password}', {self.name})"

class InkubatorsModel(Base):
    __tablename__ = "inkubators"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(10), index=True)
    min_temp = Column(Integer)
    max_temp = Column(Integer)
    min_humd = Column(Integer)
    max_humd = Column(Integer)
    water_volume = Column(Integer)
    username = Column(String(100))


class HatchDataModel(Base):
    __tablename__ = "hatch_data"

    id  = Column(Integer, primary_key=True, index=True)
    inkubator_id = Column(Integer, nullable=False)
    start_data = Column(Date)
    end_data_estimation = Column(Date)
    number_of_egg = Column(Integer)