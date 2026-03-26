from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordBearer
from app.schemas.post import PostCreate, PostOut
from app.crud import post as crud_post
from app.crud import user as crud_user
from app.db.session import get_db
from app.auth.auth import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

router = APIRouter(prefix="/posts", tags=["posts"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Get current user dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = crud_user.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Create post
@router.post("/", response_model=PostOut)
def create_new_post(post: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud_post.create_post(db, post.title, post.content, current_user)

# Read all posts
@router.get("/", response_model=List[PostOut])
def list_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_post.get_posts(db, skip, limit)

# Read single post
@router.get("/{post_id}", response_model=PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = crud_post.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Update post
@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_post = crud_post.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud_post.update_post(db, post_id, post.title, post.content)

# Delete post
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_post = crud_post.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    crud_post.delete_post(db, post_id)
    return {"detail": "Post deleted successfully"}