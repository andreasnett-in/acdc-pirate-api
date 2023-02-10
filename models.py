from sqlalchemy import Column, Integer, Float, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class LatLongHasPirate(Base):
    __tablename__ = "LatLongHasPirate"
    id = Column(Integer, primary_key=True)
    west = Column(Float, nullable=False)
    east = Column(Float, nullable=False)
    north = Column(Float, nullable=False)
    south = Column(Float, nullable=False)
    has_pirate = Column(Boolean, nullable=True)