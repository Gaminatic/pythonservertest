from fastapi import APIRouter,HTTPException
from app.database.connection import with_connection
from app.database.db import adminSignup
from jwtoken import create_access_token
from models import Signup

router = APIRouter()


@router.post("/adminSignup")
async def create_admin(s: Signup):
    try:
        print("recieved data",s)
        result = await with_connection(adminSignup,s.mailid, s.mobileno, s.username, s.password)
        print("with connection result",result)
        user_id = str(result)
        access_token = create_access_token(data={"user_id": user_id})
        if not result:
            raise HTTPException(status_code=400, detail="User creation failed")
        return {"message": "Admin created successfully", "data": result,"access_token":access_token}
    except Exception as e:
        print("exception",e)
        raise HTTPException(status_code=500, detail=str(e))