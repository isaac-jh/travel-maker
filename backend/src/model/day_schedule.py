from sqlalchemy import Column, BigInteger, Time, DateTime
from sqlalchemy.sql import func
from src.util.database import Base


class DaySchedule(Base):
    __tablename__ = "day_schedules"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    plan_id = Column(BigInteger, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

