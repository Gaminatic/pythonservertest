from fastapi import APIRouter, Depends,HTTPException
from app.database.connection import with_connection
from app.database.db import setlevel
from jwtoken import get_current_user 
from models import SetLevel

router = APIRouter()

@router.post("/setuserLevel")
async def set_user_level(l:SetLevel,access_token: str = Depends(get_current_user)):
    try:
        user_id = access_token
        user_level = await with_connection(setlevel,l.counts,user_id,l.typeid)
        return {"user_level": user_level}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))