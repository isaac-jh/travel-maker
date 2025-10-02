from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.util.database import get_db
from src.schema.user import UserSignupRequest, UserLoginRequest, UserLoginResponse, UserResponse
from src.service.user_service import create_user, login_user

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignupRequest, db: Session = Depends(get_db)):
    user = create_user(db, user_data)
    return user


@router.post("/login", response_model=UserLoginResponse)
def login(login_data: UserLoginRequest, db: Session = Depends(get_db)):
    result = login_user(db, login_data)
    return result

