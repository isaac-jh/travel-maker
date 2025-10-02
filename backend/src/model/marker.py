from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from src.util.database import Base


class Marker(Base):
    __tablename__ = "markers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    plan_id = Column(BigInteger, nullable=False)
    name = Column(String(20), nullable=True)
    description = Column(String(512), nullable=True)
    thumbnail = Column(String(512), nullable=True)
    url = Column(String(512), nullable=True)
    is_scheduled = Column(Boolean, nullable=False, server_default="0")
    created_user_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

