from APP.database import engine, get_db
from .. import models, Schemas, utilities, oauth2
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy.sql import func
models.Base.metadata.create_all(bind = engine)

router = APIRouter(
    prefix= "/users",
    tags= ["USERS"]
)
    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= Schemas.UserResponse)
def create_user(newuser: Schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utilities.passwordhasher(newuser.password)
    newuser.password = hashed_password
    new_user = models.Users(**newuser.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=Schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} not found")
    print (user)
    return user
    

@router.get("/", response_model= List[Schemas.UserFollow])
#@router.get("/")
def get_all_users(db: Session = Depends(get_db),
                  current_user:int = Depends(oauth2.get_current_user), limit:int = 6000000000, skip:int =0, search :Optional[str]=""):
    users = db.query(models.Users).filter(models.Users.Name.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Users, func.count(models.Follows.leaders).label("Followers")).join(models.Follows, models.Follows.leaders == models.Users.id, isouter= True).group_by(models.Users.id).all()
    print (results)
    return results