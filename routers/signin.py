from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import  OAuth2PasswordRequestForm
from connection import with_connection
from connection import login_user

# from jwtoken import create_access_token
router = APIRouter()

@router.post("/signin")
async def signinUser(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        print("Attempting to sign in user:", form_data.username)
        result = await with_connection(login_user, form_data.username, form_data.password)
        if not result:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        user_dict = result
        user_id = user_dict.get('userid')
        if not user_id:
            raise HTTPException(status_code=500, detail="UserID not found in response")

        # access_token = create_access_token(data={"user_id": str(user_id)})
        # print("token",access_token)
        # return {"access_token": access_token, "token_type": "bearer", "user_details": user_dict}
        return user_dict

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

