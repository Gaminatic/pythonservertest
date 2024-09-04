import uuid
import asyncpg
from fastapi import APIRouter, Depends,HTTPException
from app.database.connection import with_connection
from app.database.db import geteventList
from jwtoken import get_current_user 

router = APIRouter()

@router.get("/geteventList")
async def get_user_event_list(access_token: str = Depends(get_current_user)):
    try:
        user_id = access_token
        event_list = await with_connection(geteventList, user_id)
        if event_list is None:
            raise HTTPException(status_code=404, detail="Events not found")
        return {"event_list": event_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
