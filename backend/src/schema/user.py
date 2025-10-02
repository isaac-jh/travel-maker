from pydantic import BaseModel, Field
from datetime import datetime


class UserSignupRequest(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=40)
    password: str = Field(..., min_length=6, max_length=100)
    thumbnail: str = Field(..., max_length=1024)


class UserResponse(BaseModel):
    id: int
    nickname: str
    thumbnail: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

