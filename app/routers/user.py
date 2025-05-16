
from fastapi import FastAPI,Response,HTTPException,status,APIRouter
from app.database import SessionDep
from app import schemas,utils,models

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(session:SessionDep,user:schemas.UserCreate):

    # hashing the password user.passward
    hashed_password=utils.hashing_password(user.password)
    user.password=hashed_password

    new_user=models.Users(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int,session:SessionDep):
    user=session.get(models.Users,id)
    if user== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with {id} does not exist..")
    return user