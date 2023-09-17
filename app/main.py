from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from . import models
from .database import engine
from .routers import post, user, auth, votes

# Create database
models.Base.metadata.create_all(bind=engine)

# Create a FastAPI app
app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define API endpoints
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

# Root endpoint


@app.get("/")
def root():
    return {"message": "Welcome to my super cool API"}
    