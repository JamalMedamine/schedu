from fastapi import APIRouter, Depends
from sqlalchemy.orm import session
from utils.db import get_db
from utils.security import oauth2_scheme
from schemas.user_schemas import UserCreate, UserLogin, UserloginResponse
from services.auth_service import register_user, login_user, logout_user, refresh_access_token

router = APIRouter()

@router.post("/register/")
async def create_user(user: UserCreate, db: session = Depends(get_db)):
    new_user = await register_user(user, db)
    return {"message": "User created successfully", "user_id": new_user.id}

@router.post("/login/")
async def login(user: UserLogin, db: session = Depends(get_db)):
    tokens = await login_user(user, db)
    return UserloginResponse(**tokens)

@router.post("/logout")
async def logout(refresh_token: str ):
    return await logout_user(refresh_token)

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    return await refresh_access_token(refresh_token)