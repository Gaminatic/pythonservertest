import uuid
import asyncpg
from fastapi import APIRouter, Depends,HTTPException
from app.database.connection import with_connection
from app.database.db import eventMembers
from jwtoken import get_current_user 

router = APIRouter()

@router.get("/eventMembersByEid")
async def get_event_members(eid:str,access_token: str = Depends(get_current_user)):
    try:
        userid = access_token
        event_members = await with_connection(eventMembers, eid,access_token)
        return event_members
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))