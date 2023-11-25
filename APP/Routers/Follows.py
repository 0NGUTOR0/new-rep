from APP.database import engine, get_db
from .. import models, Schemas, oauth2
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind = engine)

router = APIRouter(
    prefix= "/follows",
    tags= ["FOLLOWS"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def follow(followuser: Schemas.Follow, db: Session = Depends(get_db), 
           current_user:int = Depends(oauth2.get_current_user)):
    user_search = db.query(models.Users).filter(models.Users.id==followuser.user).all()
    following_query = db.query(models.Follows).filter(models.Follows.followers==current_user.id, 
                                                        models.Follows.leaders==followuser.user)
    if user_search == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{followuser.user} not found")
    following_already = following_query.first()
    if (followuser.dir== 1):
        if following_already:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You are already following {models.Users.Name}")
        new_follow = models.Follows(leaders=followuser.user, followers=current_user.id)
        db.add(new_follow)
        db.commit()
        return {f"message":"You just followed {followuser.user}"}
    else: 
        if following_already == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You are not following user with id:{followuser.user}")
        following_query.delete(synchronize_session=False)
        db.commit()
        return{f"message":"You just unfollowed {followuser.user}"}