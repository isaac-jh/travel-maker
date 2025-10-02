from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class PlanCreateRequest(BaseModel):
    user_id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=512)
    city_to_stay: Optional[str] = Field(None, max_length=20)
    init_latitude: float
    init_longitude: float
    start_date: date
    end_date: date


class PlanResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    city_to_stay: Optional[str]
    init_latitude: float
    init_longitude: float
    start_date: date
    end_date: date
    created_user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

