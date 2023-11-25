import sqlalchemy
from APP.database import engine, get_db
from .. import models, Schemas, oauth2
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
models.Base.metadata.create_all(bind = engine)
from sqlalchemy.sql import func
router = APIRouter(
    prefix= "/posts",
    tags= ["POSTS"]
)
 

@router.get("/", response_model=List[Schemas.PostVoteOut])
def get_all_posts(db: Session = Depends(get_db),
                  current_user:int = Depends(oauth2.get_current_user), limit:int = 10, skip:int =0, search :Optional[str]=""):
    results = db.query(models.Post, func.count(models.Likes.post_id).label("Likes")).join(models.Likes, models.Likes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    return results
    #cursor.execute("""SELECT * FROM "POSTS" """)  
    #posts = cursor.fetchall()
    #return posts
#, func.count(models.Likes.post_id).label("Likes")
#group_by(models.Post.id).


@router.post("/", status_code=status.HTTP_201_CREATED,  response_model= Schemas.PostResponse)
def create_posts(newpost: Schemas.PostCreate, db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO "POSTS" (title, content) VALUES (%s, %s) RETURNING *""",
    #               (newpost.title, newpost.content))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(Poster=current_user.id, **newpost.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=Schemas.PostVoteOut)
def get_one_post(id: int, db: Session = Depends(get_db),
                current_user:str = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    results = db.query(models.Post, func.count(models.Likes.post_id).label("Likes")).join(models.Likes, models.Likes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if results == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    return results


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)
                ,current_user:str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #cursor.execute("""DELETE FROM "POSTS" WHERE "ID"= %s RETURNING *""" ,
    #                (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} not found")
    if post.Poster != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"how you go delete another man post Oga?")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {'post is gone nigga!'}


@router.put("/{id}", status_code=status.HTTP_201_CREATED,  response_model=Schemas.PostResponse)
def update_post(id:int, updatedpost: Schemas.PostCreate, db: Session = Depends(get_db),
                 current_user:str = Depends(oauth2.get_current_user)):
   
    #cursor.execute("""UPDATE "POSTS" SET "title" = %s, "content" =%s WHERE "ID"= %s RETURNING *""", 
    #               (updatedpost.title, updatedpost.content, str(id) ))
    #updated_post = cursor.fetchone()
    #conn.commit()
    

    # This only works this way and i dont know why. Why does the .first method have to be called on a separate line and call that variable post
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    if post.Poster != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"how you go update another man post Oga?")
    post_query.update (updatedpost.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
