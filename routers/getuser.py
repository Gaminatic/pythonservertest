from fastapi import APIRouter, HTTPException
from connection import getUsersDetails, with_connection


router = APIRouter()


@router.get("/user")
async def get_user():
    try:
        print("Attempting to get user")
        result = await with_connection(getUsersDetails)
        return result

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

