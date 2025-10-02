from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from typing import List
from collections import Counter
from src.model.schedule_slot import ScheduleSlot
from src.model.slot_voting import SlotVoting
from src.model.day_schedule import DaySchedule
from src.model.marker import Marker
from src.model.user import User
from src.schema.schedule_slot import ScheduleSlotCreateRequest, ScheduleSlotUpdateRequest


def create_schedule_slot(db: Session, slot_data: ScheduleSlotCreateRequest) -> ScheduleSlot:
    day_schedule = db.query(DaySchedule).filter(DaySchedule.id == slot_data.day_schedule_id).first()
    if not day_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일정을 찾을 수 없습니다."
        )
    
    max_order = db.query(func.max(ScheduleSlot.order_num)).filter(
        ScheduleSlot.day_schedule_id == slot_data.day_schedule_id
    ).scalar()
    
    next_order = (max_order or 0) + 1
    
    new_slot = ScheduleSlot(
        day_schedule_id=slot_data.day_schedule_id,
        name=slot_data.name,
        spending_time=slot_data.spending_time,
        need_to_reservation=slot_data.need_to_reservation,
        order_num=next_order
    )
    
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    
    return new_slot


def update_schedule_slot(db: Session, slot_id: int, slot_data: ScheduleSlotUpdateRequest) -> ScheduleSlot:
    slot = db.query(ScheduleSlot).filter(ScheduleSlot.id == slot_id).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="슬롯을 찾을 수 없습니다."
        )
    
    update_data = slot_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(slot, field, value)
    
    db.commit()
    db.refresh(slot)
    
    return slot


def delete_schedule_slot(db: Session, slot_id: int) -> bool:
    slot = db.query(ScheduleSlot).filter(ScheduleSlot.id == slot_id).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="슬롯을 찾을 수 없습니다."
        )
    
    db.delete(slot)
    db.commit()
    
    return True


def reorder_schedule_slots(db: Session, day_schedule_id: int, slot_ids: List[int]) -> List[ScheduleSlot]:
    existing_slots = db.query(ScheduleSlot).filter(
        ScheduleSlot.day_schedule_id == day_schedule_id
    ).all()
    
    if len(existing_slots) != len(slot_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"슬롯 개수가 일치하지 않습니다. 요청: {len(slot_ids)}, 실제: {len(existing_slots)}"
        )
    
    existing_slot_ids = {slot.id for slot in existing_slots}
    requested_slot_ids = set(slot_ids)
    
    if existing_slot_ids != requested_slot_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="잘못된 슬롯 ID가 포함되어 있습니다."
        )
    
    for order, slot_id in enumerate(slot_ids, start=1):
        slot = db.query(ScheduleSlot).filter(ScheduleSlot.id == slot_id).first()
        slot.order_num = order
    
    db.commit()
    
    updated_slots = db.query(ScheduleSlot).filter(
        ScheduleSlot.day_schedule_id == day_schedule_id
    ).order_by(ScheduleSlot.order_num).all()
    
    return updated_slots


def confirm_schedule_slot(db: Session, slot_id: int) -> ScheduleSlot:
    slot = db.query(ScheduleSlot).filter(ScheduleSlot.id == slot_id).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="슬롯을 찾을 수 없습니다."
        )
    
    votes = db.query(SlotVoting).filter(SlotVoting.schedule_slot_id == slot_id).all()
    
    if not votes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="투표 내역이 없어 확정할 수 없습니다."
        )
    
    marker_ids = [vote.marker_id for vote in votes]
    vote_counts = Counter(marker_ids)
    most_voted_marker_id = vote_counts.most_common(1)[0][0]
    
    slot.holding_marker_id = most_voted_marker_id
    
    db.commit()
    db.refresh(slot)
    
    return slot


def vote_schedule_slot(db: Session, slot_id: int, marker_id: int, user_id: int) -> SlotVoting:
    slot = db.query(ScheduleSlot).filter(ScheduleSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="슬롯을 찾을 수 없습니다."
        )
    
    marker = db.query(Marker).filter(Marker.id == marker_id).first()
    if not marker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="마커를 찾을 수 없습니다."
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    
    existing_vote = db.query(SlotVoting).filter(
        SlotVoting.schedule_slot_id == slot_id,
        SlotVoting.voted_user_id == user_id
    ).first()
    
    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 투표한 슬롯입니다."
        )
    
    new_vote = SlotVoting(
        schedule_slot_id=slot_id,
        marker_id=marker_id,
        voted_user_id=user_id
    )
    
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    
    return new_vote

