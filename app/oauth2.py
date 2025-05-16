from jwt.exceptions import InvalidTokenError,ExpiredSignatureError
import jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlmodel import Session,select
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
# SECRET KEY
# ALGORITHAM
# EXPIRATION TIME

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES =settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_acess_token(data:dict):
    to_encode=data.copy()

    expire=datetime.now()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_acces_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        print("Payload:", payload)

        user_id:str=payload.get("user_id")
        if user_id is None:
            raise credential_exception
        # token_data=schemas.TokenData(user_id=(user_id))
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except InvalidTokenError:
        raise credential_exception
    # return token_data
 


def get_current_user(session:database.SessionDep,token:str=Depends(oauth2_scheme)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                       detail="Could not validate credentials",
                                       headers={"WWW-Authenticate":"Bearer"})
    
    user_id=verify_acces_token(token,credential_exception)
     
    statement=select(models.Users).where(models.Users.id==user_id)
    user=session.exec(statement).first()
    return user
    

    # return token_data.user_id
    




