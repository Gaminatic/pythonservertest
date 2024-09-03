# from fastapi import FastAPI, HTTPException
# import asyncpg
# import os

# app = FastAPI()

# DATABASE_URL = "postgresql://azureuser:sevenlake%40123@fitness-db-public.postgres.database.azure.com:5432/postgres?sslmode=require"

# @app.on_event("startup")
# async def startup():
#     app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)

# @app.on_event("shutdown")
# async def shutdown():
#     await app.state.db_pool.close()


# @app.get("/")
# async def root():
#     print("inside root function")
#     return("Hello world")
    

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

from typing import List
import asyncpg
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
import os
import urllib

# Environment variables for database connection
# host_server = os.environ.get('host_server')
# db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port')))
# database_name = os.environ.get('database_name', 'fastapi')
# db_username = urllib.parse.quote_plus(str(os.environ.get('db_username')))
# db_password = urllib.parse.quote_plus(str(os.environ.get('db_password')))


DATABASE_URL = f'postgresql://azureuser:sevenlake%40123@fitness-db-public.postgres.database.azure.com:5432/postgres?sslmode=require'

# Initialize FastAPI app
app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)

@app.on_event("startup")
async def startup():
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)


@app.on_event("shutdown")
async def shutdown():
    await app.state.db_pool.close()


@app.get("/")
async def root():
    print("inside root function")
    return("Hello world")

@app.get("/users")
async def get_user_function():
    query = "SELECT * FROM users"
    print("query",query)
    print("url",DATABASE_URL)
    async with app.state.db_pool.acquire() as connection:
        user = await connection.fetchrow(query)
    return {"users data",user}






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
