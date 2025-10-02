from pydantic import BaseModel, Field
from datetime import time, date, datetime
from typing import Optional, List


class ScheduleSlotResponse(BaseModel):
    id: int
    day_schedule_id: int
    holding_marker_id: Optional[int]
    name: Optional[str]
    spending_time: time
    need_to_reservation: bool
    is_reserved: bool
    order_num: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DayScheduleCreateRequest(BaseModel):
    plan_id: int
    date: date
    start_time: time
    end_time: time


class DayScheduleUpdateRequest(BaseModel):
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None


class DayScheduleResponse(BaseModel):
    id: int
    plan_id: int
    date: date
    start_time: time
    end_time: time
    created_at: datetime
    updated_at: datetime
    schedule_slots: List[ScheduleSlotResponse] = []

    class Config:
        from_attributes = True

