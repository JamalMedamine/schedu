from fastapi import APIRouter ,Depends
from sqlalchemy.orm  import session
from models.user import User
from utils.db import get_db
from schemas.user_schemas import UserCreate 
from utils.password_hash import hash_password , verify_password
router = APIRouter()

@router.post("/users/")
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
