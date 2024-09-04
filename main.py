from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from app.database.connection import acquire_connection, close_pool
from routers.login import router as signin
from routers.signup import router as signup



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

app.include_router(signin,tags = ["userLogin"])
app.include_router(signup,tags = ["userSignup"])




@app.get("/")
async def read_root():
    return {"message": "Hii From tn"}


if __name__ == "__main__":
    print("host",os.getenv("HOST"))
    uvicorn.run(app,host=os.getenv("HOST"),port=int(os.getenv("PORT")))
