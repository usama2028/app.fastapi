
from fastapi import FastAPI,APIRouter,HTTPException,Response,status,Depends
from app import schemas,database,models,utils,oauth2
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select



router=APIRouter(
    tags=["Authentication"]
)

@router.post("/login",response_model=schemas.Token)
def login(session:database.SessionDep,creditentials:OAuth2PasswordRequestForm=Depends()):
    statement = select(models.Users).where(models.Users.email == creditentials.username)
    user = session.exec(statement).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credientials")
    if not utils.verify(creditentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credientials")
    
    # create tokens
    acess_token=oauth2.create_acess_token(data={"user_id":user.id})

    # return token

    return {"token":acess_token,"token_type":"bearer"}
