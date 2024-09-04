from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from app.database.connection import acquire_connection, close_pool
from routers.signup import router as signup
from routers.createAdmin import router as adminsignup
from routers.getActivities import router as get_Activities
from routers.createActy import router as Activity
from routers.updateActy import router as updateActivity
from routers.deleteActy import router as deleteActivity
from routers.login import router as signin
from routers.getLevel import router as getuserlevel
from routers.eventCount import router as insertEventCount
from routers.geteventList import router as eventList
from routers.geteMembers import router as eventmembers
from routers.setLevel import router as set_Level 




load_dotenv()

app =  FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("database",os.getenv("PGDATABASE"))
    await acquire_connection()

    try:
        yield
    finally:
        await close_pool()


app = FastAPI(lifespan=lifespan)


app.include_router(adminsignup,tags=['adminSignup'])
app.include_router(get_Activities,tags=['getActivitiy'])
app.include_router(Activity,tags=['CreateActivity'])
app.include_router(updateActivity,tags=['updateActivity'])
app.include_router(deleteActivity,tags=['deleteActivity'])



app.include_router(signup,tags = ["userCreation"])
app.include_router(signin,tags = ["userLogin"])
app.include_router(getuserlevel,tags = ["getUserLevels"])
app.include_router(insertEventCount,tags=["EventCounts"])
app.include_router(eventList,tags = ["geteventList"])
app.include_router(eventmembers,tags=["geteventMembersList"])
app.include_router(set_Level,tags = ["setUserLevel"])





@app.get("/")
async def read_root():
    return {"message": "Hii From tn"}


if __name__ == "__main__":
    print("host",os.getenv("HOST"))
    uvicorn.run(app,host=os.getenv("HOST"),port=int(os.getenv("PORT")))
