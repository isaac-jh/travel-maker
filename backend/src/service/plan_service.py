from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from src.model.plan import Plan
from src.model.users_in_plan import UsersInPlan
from src.model.user import User
from src.schema.plan import PlanCreateRequest, PlanUpdateRequest


def create_plan(db: Session, plan_data: PlanCreateRequest) -> Plan:
    user = db.query(User).filter(User.id == plan_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    
    if plan_data.start_date > plan_data.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="시작일은 종료일보다 이전이어야 합니다."
        )
    
    new_plan = Plan(
        name=plan_data.name,
        description=plan_data.description,
        city_to_stay=plan_data.city_to_stay,
        init_latitude=plan_data.init_latitude,
        init_longitude=plan_data.init_longitude,
        start_date=plan_data.start_date,
        end_date=plan_data.end_date,
        created_user_id=plan_data.user_id
    )
    
    db.add(new_plan)
    db.flush()
    
    users_in_plan = UsersInPlan(
        user_id=plan_data.user_id,
        plan_id=new_plan.id,
        owner=True
    )
    
    db.add(users_in_plan)
    db.commit()
    db.refresh(new_plan)
    
    return new_plan


def get_plans_by_user(db: Session, user_id: int) -> List[Plan]:
    plans = db.query(Plan).join(
        UsersInPlan, 
        Plan.id == UsersInPlan.plan_id
    ).filter(
        UsersInPlan.user_id == user_id,
        Plan.is_deleted == False
    ).all()
    
    return plans


def get_all_plans(db: Session, keyword: Optional[str] = None) -> List[Plan]:
    query = db.query(Plan).filter(Plan.is_deleted == False)
    
    if keyword:
        query = query.filter(Plan.name.like(f"%{keyword}%"))
    
    plans = query.all()
    return plans


def join_plan(db: Session, plan_id: int, user_id: int) -> UsersInPlan:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="플랜을 찾을 수 없습니다."
        )
    
    if plan.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="삭제된 플랜에는 참가할 수 없습니다."
        )
    
    existing = db.query(UsersInPlan).filter(
        UsersInPlan.user_id == user_id,
        UsersInPlan.plan_id == plan_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 참가한 플랜입니다."
        )
    
    users_in_plan = UsersInPlan(
        user_id=user_id,
        plan_id=plan_id,
        owner=False
    )
    
    db.add(users_in_plan)
    db.commit()
    db.refresh(users_in_plan)
    
    return users_in_plan


def update_plan(db: Session, plan_id: int, plan_data: PlanUpdateRequest) -> Plan:
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="플랜을 찾을 수 없습니다."
        )
    
    if plan.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="삭제된 플랜입니다."
        )
    
    update_data = plan_data.model_dump(exclude_unset=True)
    
    if "start_date" in update_data or "end_date" in update_data:
        start_date = update_data.get("start_date", plan.start_date)
        end_date = update_data.get("end_date", plan.end_date)
        
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="시작일은 종료일보다 이전이어야 합니다."
            )
    
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    db.commit()
    db.refresh(plan)
    
    return plan


def delete_plan(db: Session, plan_id: int, user_id: int) -> bool:
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="플랜을 찾을 수 없습니다."
        )
    
    if plan.created_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="플랜을 삭제할 권한이 없습니다."
        )
    
    if plan.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 삭제된 플랜입니다."
        )
    
    plan.is_deleted = True
    db.commit()
    
    return True


def transfer_ownership(db: Session, plan_id: int, old_owner: int, new_owner: int) -> bool:
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="플랜을 찾을 수 없습니다."
        )
    
    if plan.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="삭제된 플랜입니다."
        )
    
    old_owner_record = db.query(UsersInPlan).filter(
        UsersInPlan.plan_id == plan_id,
        UsersInPlan.user_id == old_owner
    ).first()
    
    if not old_owner_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="기존 소유자를 찾을 수 없습니다."
        )
    
    if not old_owner_record.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="소유자만 권한을 넘길 수 있습니다."
        )
    
    new_owner_record = db.query(UsersInPlan).filter(
        UsersInPlan.plan_id == plan_id,
        UsersInPlan.user_id == new_owner
    ).first()
    
    if not new_owner_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="새 소유자가 플랜에 참가하지 않았습니다."
        )
    
    old_owner_record.owner = False
    new_owner_record.owner = True
    
    db.commit()
    
    return True

