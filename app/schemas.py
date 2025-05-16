
from pydantic import  BaseModel,EmailStr,conint
from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

class PostCreate(BaseModel):
    title:str
    content:str
    publish:bool=True

class PostResponse(PostCreate):
    id:int
    created_at:datetime
    user_id:int
    owner:UserResponse

class PostOut(BaseModel):
    Post:PostResponse
    votes:int



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    token:str
    token_type:str


class TokenData(BaseModel):
    user_id:Optional[str]=None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) 





    
