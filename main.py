from fastapi import FastAPI
from app.db.session import engine, Base

# You must include 'api' in the path now
from app.routes.user import router as user_router
from app.routes.post import router as post_router

# Import models so SQLAlchemy creates them
from app.models.user import User
from app.models.post import Post

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Social Media API")

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(post_router, prefix="/posts", tags=["Posts"])