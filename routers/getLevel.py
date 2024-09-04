import uuid
import asyncpg
from fastapi import APIRouter, Depends,HTTPException
from app.database.connection import with_connection
from app.database.db import getlevel
from jwtoken import get_current_user 

router = APIRouter()

@router.get("/getuserLevel")
async def get_user_levels(access_token: str = Depends(get_current_user)):
    try:
        user_id = access_token
        user_level = await with_connection(getlevel, user_id)
        if user_level is None:
            raise HTTPException(status_code=404, detail="User level not found")
        return {"user_level": user_level}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))