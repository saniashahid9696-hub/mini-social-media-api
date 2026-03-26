from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.user import User

def create_post(db: Session, title: str, content: str, user: User):
    post = Post(title=title, content=content, author=user)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post_id: int, title: str, content: str):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.title = title
        post.content = content
        db.commit()
        db.refresh(post)
    return post

def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
    return post