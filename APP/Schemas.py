from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
class PostCreate (BaseModel):
    title: str
    content: str
    Published: bool=True

class UserResponse(BaseModel):
    Name : str
    email : EmailStr
    Created_at: datetime
    class Config:
        orm_mode = True

class UserFollow(BaseModel):
    Users: UserResponse
    Followers: int
    class Config:
        orm_mode = True

class Owner(BaseModel):
    Name: str

class PostResponse (BaseModel):
    id: int
    title: str
    content: str
    Published: bool=True
    Created_at: datetime
    Poster: int
    Owner : UserResponse
    class Config:
        orm_mode = True

class PostVoteOut(BaseModel):
    Post: PostResponse
    Likes: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    Name : str 
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type: str

class Tokendata(BaseModel):
    id : Optional[str]=None

class Like(BaseModel):
    post:int
    dir:conint(le=1)

class Follow(BaseModel):
    user:int
    dir: conint(le=1)


