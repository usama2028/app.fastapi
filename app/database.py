
from sqlmodel import SQLModel,create_engine,Session,Field
from fastapi import Depends
from typing import Annotated
from .config import settings


connection_string=f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"


engine=create_engine(connection_string)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]