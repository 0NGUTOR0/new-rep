from APP.database import engine
from .import models
from fastapi import FastAPI
from .Routers import Follows, Posts, Users, Authentication, Likes
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind = engine)
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Posts.router)
app.include_router(Users.router)
app.include_router(Authentication.router)
app.include_router(Likes.router)
app.include_router(Follows.router)

@app.get("/")
def root():
    return {"message":"whatsup life"}