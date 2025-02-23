from fastapi import FastAPI
from .routers import posts, users
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)