from sqlalchemy import Column, BigInteger, Boolean, DateTime
from sqlalchemy.sql import func
from src.util.database import Base


class UsersInPlan(Base):
    __tablename__ = "users_in_plan"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    plan_id = Column(BigInteger, nullable=False)
    owner = Column(Boolean, nullable=False, server_default="0")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

