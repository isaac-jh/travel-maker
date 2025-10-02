from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.util.database import get_db
from src.schema.schedule_slot import (
    ScheduleSlotCreateRequest, 
    ScheduleSlotUpdateRequest, 
    ScheduleSlotResponse,
    ReorderSlotsRequest,
    VoteSlotRequest
)
from src.service.schedule_slot_service import (
    create_schedule_slot,
    update_schedule_slot,
    delete_schedule_slot,
    reorder_schedule_slots,
    confirm_schedule_slot,
    vote_schedule_slot
)

router = APIRouter()


@router.post("", response_model=ScheduleSlotResponse, status_code=status.HTTP_201_CREATED)
def create_new_schedule_slot(slot_data: ScheduleSlotCreateRequest, db: Session = Depends(get_db)):
    slot = create_schedule_slot(db, slot_data)
    return slot


@router.put("/{slot_id}", response_model=ScheduleSlotResponse)
def update_existing_schedule_slot(slot_id: int, slot_data: ScheduleSlotUpdateRequest, db: Session = Depends(get_db)):
    slot = update_schedule_slot(db, slot_id, slot_data)
    return slot


@router.delete("/{slot_id}")
def delete_existing_schedule_slot(slot_id: int, db: Session = Depends(get_db)):
    result = delete_schedule_slot(db, slot_id)
    return {"success": result, "message": "슬롯이 삭제되었습니다."}


@router.post("/reorder", response_model=List[ScheduleSlotResponse])
def reorder_slots(reorder_data: ReorderSlotsRequest, db: Session = Depends(get_db)):
    slots = reorder_schedule_slots(db, reorder_data.day_schedule_id, reorder_data.slot_ids)
    return slots


@router.post("/{slot_id}/confirm", response_model=ScheduleSlotResponse)
def confirm_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = confirm_schedule_slot(db, slot_id)
    return slot


@router.post("/vote")
def vote_slot(vote_data: VoteSlotRequest, db: Session = Depends(get_db)):
    result = vote_schedule_slot(db, vote_data.schedule_slot_id, vote_data.marker_id, vote_data.user_id)
    return {"success": True, "message": "투표가 완료되었습니다.", "vote_id": result.id}

