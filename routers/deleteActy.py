from fastapi import APIRouter, Depends,HTTPException
from app.database.connection import with_connection
from app.database.db import deleteActivities
from jwtoken import get_current_user 
from models import DltActivities

router = APIRouter()

@router.put("/deleteActivities")
async def delete_activities(d:DltActivities,access_token: str = Depends(get_current_user)):
    try:
        adminid = access_token
        Activities = await with_connection(deleteActivities,adminid,d.id)
        return Activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))