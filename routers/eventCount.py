from fastapi import APIRouter, Depends,HTTPException
from app.database.connection import with_connection
from app.database.db import inserteventCounts
from jwtoken import get_current_user 
from models import eventLogs

router = APIRouter()

@router.post("/insertEventCounts")
async def event_logs(e:eventLogs,access_token: str = Depends(get_current_user)):
    try:
        user_id = access_token
        eventLogs = await with_connection(inserteventCounts,user_id,e.eid,e.counts)
        return eventLogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))