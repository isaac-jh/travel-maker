import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.model.user import User
from src.schema.user import UserSignupRequest


def check_nickname_duplicate(db: Session, nickname: str) -> bool:
    existing_user = db.query(User).filter(User.nickname == nickname).first()
    return existing_user is not None


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_user(db: Session, user_data: UserSignupRequest) -> User:
    if check_nickname_duplicate(db, user_data.nickname):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 닉네임입니다."
        )
    
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        nickname=user_data.nickname,
        password=hashed_password,
        thumbnail=user_data.thumbnail
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

