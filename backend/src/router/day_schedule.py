from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from src.util.database import get_db
from src.schema.day_schedule import DayScheduleCreateRequest, DayScheduleUpdateRequest, DayScheduleResponse
from src.service.day_schedule_service import create_day_schedule, get_day_schedules_by_plan, update_day_schedule, delete_day_schedule

router = APIRouter()


@router.post("", response_model=DayScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_new_day_schedule(schedule_data: DayScheduleCreateRequest, db: Session = Depends(get_db)):
    schedule = create_day_schedule(db, schedule_data)
    return schedule


@router.get("", response_model=List[DayScheduleResponse])
def get_day_schedules(plan_id: int = Query(...), db: Session = Depends(get_db)):
    schedules = get_day_schedules_by_plan(db, plan_id)
    return schedules


@router.put("/{schedule_id}", response_model=DayScheduleResponse)
def update_existing_day_schedule(schedule_id: int, schedule_data: DayScheduleUpdateRequest, db: Session = Depends(get_db)):
    schedule = update_day_schedule(db, schedule_id, schedule_data)
    return schedule


@router.delete("/{schedule_id}")
def delete_existing_day_schedule(schedule_id: int, db: Session = Depends(get_db)):
    result = delete_day_schedule(db, schedule_id)
    return {"success": result, "message": "일정이 삭제되었습니다."}

