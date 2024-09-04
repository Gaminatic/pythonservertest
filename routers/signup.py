from fastapi import APIRouter, Depends, HTTPException
from app.database.connection import with_connection
from app.database.connection import signup
from jwtoken import create_access_token
from models import Signup

router = APIRouter()



@router.post("/signup")
async def create_user(s: Signup):
    try:
        result = await with_connection(signup, s.mailid, s.mobileno, s.username, s.password)
        user_id = str(result)
        access_token = create_access_token(data={"user_id": user_id})

        if not result:
            raise HTTPException(status_code=400, detail="User creation failed")
        return {"message": "User created successfully", "data": result,"access_token":access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))