import uuid
import asyncpg
from fastapi import APIRouter, Depends, HTTPException,Request
from fastapi.responses import JSONResponse
from app.database.connection import with_connection
from app.database.db import getActivities
from jwtoken import get_current_user 

router = APIRouter()

@router.get("/get_Activities")
async def get_Activities(request: Request, access_token: str = Depends(get_current_user)):
    try:
        user_id = access_token
        activities = await with_connection(getActivities, user_id)
        print("before", activities)
        custom_etag = f"activities-{user_id}"
        headers = {
            "Cache-Control": "public",
            "ETag": custom_etag
        }
        print("cache")
        if_none_match = request.headers.get("If-None-Match")
        if if_none_match == custom_etag:
            return JSONResponse(status_code=304, headers=headers)

        return JSONResponse(content=activities, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

