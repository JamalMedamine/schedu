from fastapi import FastAPI
from routers import auth_router
from utils.db import Base, engine, init_db

app = FastAPI()
app.include_router(auth_router.router)
