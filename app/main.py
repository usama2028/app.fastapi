from fastapi import FastAPI
from app.database import create_db_and_tables
from .routers import posts,user,authentication,vote
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()


origion=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origion,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return{"message":"hello users"}
