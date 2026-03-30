from datetime import datetime
from sqlalchemy.orm import Session 
from sqlalchemy import select 
from models.user import User
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token, create_refresh_token, verify_token, blacklist_token , is_token_blacklisted
from fastapi import HTTPException

async def register_user(user_data, db: Session):
    try:
        hashed_password = hash_password(user_data.password)
        new_user = User(
            firstName=user_data.firstName,
            lastName=user_data.lastName,
            email=user_data.email,
            password=hashed_password
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")

async def login_user(user_data, db: Session):
    try:
        stmt = select(User).where(User.email == user_data.email)  
        result = await db.execute(stmt)               
        db_user = result.scalars().first() 
        if not db_user or not verify_password(user_data.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        access_token = create_access_token({"sub": db_user.email})
        refresh_token = create_refresh_token({"sub": db_user.email})
        return {"access_token": access_token, "refresh_token": refresh_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

async def logout_user(refresh_token: str):
    try:
        payload = verify_token(refresh_token)
        exp = payload.get("exp")
        expires_in = max(exp - int(datetime.utcnow().timestamp()), 0)
        await blacklist_token(refresh_token, expires_in)
        return {"msg": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")

async def refresh_access_token(refresh_token: str):
    try:
        payload = verify_token(refresh_token)
        email = payload.get("sub")
        if not email or payload.get("type") != "refresh" or await is_token_blacklisted(refresh_token):
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        new_access_token = create_access_token({"sub": email})
        return {"access_token": new_access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token refresh failed: {str(e)}")