from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from typing import List
from src.model.day_schedule import DaySchedule
from src.model.schedule_slot import ScheduleSlot
from src.model.plan import Plan
from src.schema.day_schedule import DayScheduleCreateRequest, DayScheduleUpdateRequest


def create_day_schedule(db: Session, schedule_data: DayScheduleCreateRequest) -> DaySchedule:
    plan = db.query(Plan).filter(Plan.id == schedule_data.plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="플랜을 찾을 수 없습니다."
        )
    
    if plan.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="삭제된 플랜에는 일정을 추가할 수 없습니다."
        )
    
    existing_schedule = db.query(DaySchedule).filter(
        DaySchedule.plan_id == schedule_data.plan_id,
        DaySchedule.date == schedule_data.date
    ).first()
    
    if existing_schedule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="해당 날짜에 이미 일정이 존재합니다."
        )
    
    if schedule_data.start_time >= schedule_data.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="시작 시간은 종료 시간보다 이전이어야 합니다."
        )
    
    new_schedule = DaySchedule(
        plan_id=schedule_data.plan_id,
        date=schedule_data.date,
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time
    )
    
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    
    return new_schedule


def get_day_schedules_by_plan(db: Session, plan_id: int) -> List[DaySchedule]:
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="플랜을 찾을 수 없습니다."
        )
    
    schedules = db.query(DaySchedule).options(
        joinedload(DaySchedule.schedule_slots)
    ).filter(
        DaySchedule.plan_id == plan_id
    ).all()
    
    return schedules


def update_day_schedule(db: Session, schedule_id: int, schedule_data: DayScheduleUpdateRequest) -> DaySchedule:
    schedule = db.query(DaySchedule).filter(DaySchedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일정을 찾을 수 없습니다."
        )
    
    update_data = schedule_data.model_dump(exclude_unset=True)
    
    if "start_time" in update_data or "end_time" in update_data:
        start_time = update_data.get("start_time", schedule.start_time)
        end_time = update_data.get("end_time", schedule.end_time)
        
        if start_time >= end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="시작 시간은 종료 시간보다 이전이어야 합니다."
            )
    
    for field, value in update_data.items():
        setattr(schedule, field, value)
    
    db.commit()
    db.refresh(schedule)
    
    return schedule


def delete_day_schedule(db: Session, schedule_id: int) -> bool:
    schedule = db.query(DaySchedule).filter(DaySchedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일정을 찾을 수 없습니다."
        )
    
    db.delete(schedule)
    db.commit()
    
    return True

