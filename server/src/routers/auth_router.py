from datetime import datetime
from utils.security import oauth2_scheme
from fastapi import APIRouter ,Depends, HTTPException
from sqlalchemy.orm  import session
from models.user import User
from utils.db import get_db
from utils.redis import blacklist_token
from schemas.user_schemas import UserCreate , UserLogin , UserloginResponse
from utils.security import hash_password , verify_password
from utils.jwt import create_access_token , create_refresh_token , verify_token
import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

router = APIRouter()

@router.post("/register/")
async def create_user(user: UserCreate, db: session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}


@router.post("/login/")
async def login(user: UserLogin, response: UserloginResponse, db: session = Depends(get_db)):
    db_user = await db.execute(
        session.query(User).filter(User.email == user.email)
    )
    db_user = db_user.scalars().first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})
    return UserloginResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    # calculate seconds until token expires
    exp = payload.get("exp")
    expires_in = max(exp - int(datetime.utcnow().timestamp()), 0)
    await blacklist_token(token, expires_in)
    return {"msg": "Logged out successfully"}

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    new_access_token = create_access_token({"sub": email})
    return {"access_token": new_access_token}