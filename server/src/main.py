from fastapi import FastAPI
from routers import users_router
from utils.db import Base, engine, init_db

app = FastAPI()
app.include_router(users_router.router)
