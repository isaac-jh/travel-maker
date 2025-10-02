from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from src.util.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nickname = Column(String(40), nullable=False)
    password = Column(String(200), nullable=False)
    thumbnail = Column(String(1024), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

