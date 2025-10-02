from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.model.plan import Plan
from src.model.users_in_plan import UsersInPlan
from src.model.user import User
from src.schema.plan import PlanCreateRequest


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

