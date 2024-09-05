# import os

# from flask import (Flask, redirect, render_template, request,
#                    send_from_directory, url_for)

# app = Flask(__name__)


# @app.route('/')
# def index():
#    print('Request for index page received')
#    return ('hello, I am running')



# if __name__ == '__main__':
#    app.run()

from contextlib import asynccontextmanager
import os
import asyncpg
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
# from connection import db_url,getUsersDetails
# from connection import create_pool_connection
# from connection import DatabaseConnection, getUsersDetails

app = FastAPI()
load_dotenv()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("database",os.getenv("PGDATABASE"))
#     print("db url",db_url)
#     await acquire_connection()
#     print(asyncpg.__version__)
#     try:
#         yield
#     finally:
#         await close_pool()


# app = FastAPI(lifespan=lifespan)

class DatabaseConnection:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    async def get_pool(self):
        if self._pool is None:
            print("Creating new connection pool")
            db_uri = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
            print("url",db_uri)
            self._pool = await asyncpg.create_pool(dsn=db_uri,timeout = 60)
        else:
            print("Reusing existing connection pool")
        return self._pool

    async def close_pool(self):
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
            print("Connection pool closed")

async def getUsersDetails(connection):
    try:
        users = await connection.fetchrow("SELECT * FROM users")
        return users
    except asyncpg.PostgresError as e:
        raise e

db_connection = DatabaseConnection()

@app.get("/")
def root():
   print("Inside function")
   print("db_uri",os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING'))
   return("Hello world")


@app.get("/getUsers")
async def get_users():
    pool = await db_connection.get_pool()  
    async with pool.acquire() as connection:
        users = await getUsersDetails(connection)
    return users


if __name__ == '__main__':
   uvicorn.run(app,host="0.0.0.0",port=8000)
