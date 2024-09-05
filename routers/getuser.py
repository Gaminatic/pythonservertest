from fastapi import APIRouter, Depends, HTTPException
from connection import getUsersDetails, with_connection
from jwtoken import get_current_user


router = APIRouter()


@router.get("/user")
async def get_user(access_token: str = Depends(get_current_user)):
    try:
        print("Attempting to get user")
        result = await with_connection(getUsersDetails)
        return result

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

