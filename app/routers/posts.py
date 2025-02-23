from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, auth, database
from typing import List
from cachetools import TTLCache

router = APIRouter(prefix="/posts", tags=["posts"])
cache = TTLCache(maxsize=1000, ttl=300)

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(request: schemas.PostRequest, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    post = models.Post(text=request.text, user_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    cache.pop(current_user.email, None)
    return post

@router.get("/", response_model=List[schemas.PostResponse])
def read_posts(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if current_user.email in cache:
        return cache[current_user.email]
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    cache[current_user.email] = posts
    return posts

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.user_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    cache.pop(current_user.email, None)