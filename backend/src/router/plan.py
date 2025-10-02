from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.util.database import get_db
from src.schema.plan import PlanCreateRequest, PlanUpdateRequest, PlanResponse
from src.service.plan_service import create_plan, get_plans_by_user, get_all_plans, update_plan, delete_plan, join_plan, transfer_ownership

router = APIRouter()


@router.post("", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_new_plan(plan_data: PlanCreateRequest, db: Session = Depends(get_db)):
    plan = create_plan(db, plan_data)
    return plan


@router.get("/all", response_model=List[PlanResponse])
def get_all_plans_list(keyword: Optional[str] = Query(None), db: Session = Depends(get_db)):
    plans = get_all_plans(db, keyword)
    return plans


@router.get("", response_model=List[PlanResponse])
def get_plans(user_id: int = Query(...), db: Session = Depends(get_db)):
    plans = get_plans_by_user(db, user_id)
    return plans


@router.post("/{plan_id}/join")
def join_existing_plan(plan_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    result = join_plan(db, plan_id, user_id)
    return {"success": True, "message": "플랜에 참가했습니다.", "users_in_plan_id": result.id}


@router.post("/{plan_id}/transfer")
def transfer_plan_ownership(
    plan_id: int, 
    old_owner: int = Query(...), 
    new_owner: int = Query(...), 
    db: Session = Depends(get_db)
):
    result = transfer_ownership(db, plan_id, old_owner, new_owner)
    return {"success": result, "message": "소유자가 변경되었습니다."}


@router.put("/{plan_id}", response_model=PlanResponse)
def update_existing_plan(plan_id: int, plan_data: PlanUpdateRequest, db: Session = Depends(get_db)):
    plan = update_plan(db, plan_id, plan_data)
    return plan


@router.delete("/{plan_id}")
def delete_existing_plan(plan_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    result = delete_plan(db, plan_id, user_id)
    return {"success": result, "message": "플랜이 삭제되었습니다."}

