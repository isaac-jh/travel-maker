from sqlalchemy import Column, BigInteger, String, Double, Date, DateTime
from sqlalchemy.sql import func
from src.util.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(512), nullable=True)
    city_to_stay = Column(String(20), nullable=True)
    init_latitude = Column(Double, nullable=False)
    init_longitude = Column(Double, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

