from fastapi import APIRouter, Depends,HTTPException
from app.database.connection import with_connection
from app.database.db import createActivities
from jwtoken import get_current_user 
from models import Activities, SetLevel

router = APIRouter()

@router.post("/create_activity")
async def create_activities(a:Activities,access_token: str = Depends(get_current_user)):
    try:
        adminid = access_token
        Activities = await with_connection(createActivities,adminid,a.name)
        return Activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))