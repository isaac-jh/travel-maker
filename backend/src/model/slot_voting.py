from sqlalchemy import Column, BigInteger, DateTime
from sqlalchemy.sql import func
from src.util.database import Base


class SlotVoting(Base):
    __tablename__ = "slot_voting"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    schedule_slot_id = Column(BigInteger, nullable=False)
    marker_id = Column(BigInteger, nullable=False)
    voted_user_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

