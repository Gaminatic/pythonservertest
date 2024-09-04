from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
import asyncpg

from connection import with_connection


SECRET_KEY = "e3369555e7cd9b1e3b968fa329d92eb85c4487d5f20a3e41facf28ddbbb47f23"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def authenticate_user(username, password):
    async with with_connection(lambda conn: conn.fetchrow(
            "SELECT userid, username, password FROM users WHERE username = $1", username)) as user_data:
        if user_data and verify_password(password, user_data["password"]):
            return {"sub": username, "user_id": user_data["userid"]}
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    print("Inside get current function")
    print("payload", payload)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    print("Userid", user_id)
    if not user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    return user_id