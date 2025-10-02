from pydantic import BaseModel, Field
from datetime import time, datetime
from typing import Optional, List


class ScheduleSlotCreateRequest(BaseModel):
    day_schedule_id: int
    name: Optional[str] = Field(None, max_length=100)
    spending_time: time
    need_to_reservation: bool = False


class ScheduleSlotUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    spending_time: Optional[time] = None
    need_to_reservation: Optional[bool] = None
    is_reserved: Optional[bool] = None


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


class ReorderSlotsRequest(BaseModel):
    day_schedule_id: int
    slot_ids: List[int]


class VoteSlotRequest(BaseModel):
    schedule_slot_id: int
    marker_id: int
    user_id: int

