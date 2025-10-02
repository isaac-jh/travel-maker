from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.util.database import get_db
from src.schema.plan import PlanCreateRequest, PlanResponse
from src.service.plan_service import create_plan

router = APIRouter()


@router.post("", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_new_plan(plan_data: PlanCreateRequest, db: Session = Depends(get_db)):
    plan = create_plan(db, plan_data)
    return plan

