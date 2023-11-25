from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import Schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .Config import settings

oauth2_Schema = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = {settings.ACCESS_TOKEN_EXPIRE_MINUTES}


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode (to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def verify_access_token(token:str, credentials_excpetion):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str =payload.get("users_ID")
        if id == None :
            raise credentials_excpetion
        token_data = Schemas.Tokendata(id = id) 
    except JWTError:
        raise credentials_excpetion
    return token_data
    
def get_current_user(token:str = Depends(oauth2_Schema), 
                     db: Session = Depends(database.get_db)):
    credentials_excpetion = HTTPException (status_code= status.HTTP_401_UNAUTHORIZED, 
                                          detail= "could not validate credentials",
                                          headers={"WWW-Authenticate":"bearer"})
    token = verify_access_token(token, credentials_excpetion)
    current_user = db.query(models.Users).filter(models.Users.id==token.id).first()
    return current_user
    
