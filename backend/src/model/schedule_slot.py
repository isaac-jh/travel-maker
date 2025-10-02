from sqlalchemy import Column, BigInteger, String, Time, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from src.util.database import Base


class ScheduleSlot(Base):
    __tablename__ = "schedule_slots"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    day_schedule_id = Column(BigInteger, ForeignKey('day_schedules.id', ondelete='CASCADE'), nullable=False)
    holding_marker_id = Column(BigInteger, nullable=True)
    name = Column(String(100), nullable=True)
    spending_time = Column(Time, nullable=False)
    need_to_reservation = Column(Boolean, nullable=False, server_default="0")
    is_reserved = Column(Boolean, nullable=False, server_default="0")
    order_num = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

