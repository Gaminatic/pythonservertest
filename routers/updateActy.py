from fastapi import APIRouter, Depends,HTTPException
from app.database.connection import with_connection
from app.database.db import updateactivities
from jwtoken import get_current_user 
from models import UpdateActivities

router = APIRouter()

@router.put("/updateActivities")
async def update_activities(a:UpdateActivities,access_token: str = Depends(get_current_user)):
    try:
        adminid = access_token
        Activities = await with_connection(updateactivities,adminid,a.id,a.name)
        return Activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))