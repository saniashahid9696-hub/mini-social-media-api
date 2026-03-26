from pydantic import BaseModel, Field
from datetime import datetime
from .user import UserOut

class PostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=5)

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: UserOut

    class Config:
        orm_mode = True