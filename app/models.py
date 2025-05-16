
from sqlmodel import SQLModel,Field,Column,ForeignKey,Relationship
from sqlalchemy import Boolean,DateTime,text
from datetime import datetime
from typing import Optional,List

posts: List["Posts"] = Relationship(back_populates="owner")

class Posts(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True,nullable=False)
    title:str=Field(nullable=False)
    content:str=Field(nullable=False)
    publish: bool = Field(
        default=True,
        sa_column=Column(Boolean, server_default=text('true'))
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime, 
            server_default=text('CURRENT_TIMESTAMP')
        )
    )
    user_id:int=Field(
        sa_column=Column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    )
    owner: Optional["Users"] = Relationship(back_populates="posts")


class Users(SQLModel,table=True):
    id:Optional[int]=Field(primary_key=True,nullable=False,default=None)
    email:str=Field(nullable=False,unique=True)
    password:str=Field(nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime, 
            server_default=text('CURRENT_TIMESTAMP')))
    posts: List["Posts"] = Relationship(back_populates="owner")

class Vote(SQLModel,table=True):
        post_id:int=Field(primary_key=True,foreign_key="posts.id",ondelete="CASCADE",nullable=False)
        user_id:int=Field(primary_key=True,foreign_key="users.id",ondelete="CASCADE",nullable=False)

class Config:
        arbitrary_types_allowed = True