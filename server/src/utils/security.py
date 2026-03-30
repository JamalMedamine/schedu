from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.jwt import verify_token , is_token_blacklisted

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if await is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token has been revoked")
    payload = verify_token(token)
    return payload