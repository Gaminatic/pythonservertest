from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import asyncpg
import os
from dotenv import load_dotenv
import psycopg2
from routers.getuser import router as getUsers
from connection import acquire_connection, close_pool, getUsersDetails, with_connection
load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
# @app.on_event("startup")
# async def startup():
#     app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)

# @app.on_event("shutdown")
# async def shutdown():
#     await app.state.db_pool.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("database",os.getenv("PGDATABASE"))
    print("db url",DATABASE_URL)
    await acquire_connection()
    print(asyncpg.__version__)
    try:
        yield
    finally:
        await close_pool()


app = FastAPI(lifespan=lifespan)

app.include_router(getUsers,tags=['users getting'])



@app.get("/")
async def root():
    print("inside root function")
    return("Root function")
    
@app.get("/users")
async def get_user():
    print("inside get user function")
    users = await with_connection(getUsersDetails)
    return users



# @app.get("/users")
# async def get_Users():
#     print("before get connection")
#     async with app.state.db_pool.acquire() as connection:
#         print("get user funct",DATABASE_URL)
#         query = "SELECT * FROM users"
#         result = await connection.fetchrow(query)
#         if result:
#             return dict(result)
#         else:
#             raise HTTPException(status_code=404, detail="user not found")








if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




