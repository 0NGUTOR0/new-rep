from APP.database import engine, get_db
from .. import models, Schemas, oauth2
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind = engine)

router = APIRouter(
    prefix= "/likes",
    tags= ["LIKES"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def like_post(likepost: Schemas.Like, db: Session = Depends(get_db),
            current_user:int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Likes).filter(models.Likes.post_id == likepost.post,
                                                models.Likes.user_id == current_user.id)
    post_search = db.query(models.Post).filter(models.Post.id==likepost.post).all()
    if  not post_search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{likepost.post} not found")
    found_vote = vote_query.first()
    if (likepost.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail= f"{current_user.Name} has already liked post {likepost.post}")
        new_like = models.Likes(post_id = likepost.post, user_id = current_user.id)
        db.add(new_like)
        db.commit()       
        return {f"message: Post liked."} 
    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with ID:{id} not found")
        vote_query.delete(synchronize_session = False)
        db.commit()
        return{"message: Like deleted."} 
    