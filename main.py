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
from connection import db_url,getUsersDetails

from connection import create_pool_connection

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


# @app.get("/")
# def root():
#    print("Inside function",os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING'))
#    return("Hello world")


# @app.get("/getUsers")
# async def get_users():
#    print("Inside function get_users")
#    pool = await create_pool_connection(pool)
#    users = await getUsersDetails()
#    return users



from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn
import logging
import os
import asyncpg
import ssl
 
app = FastAPI()
load_dotenv()
 
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
 
@app.get("/")
def root():
   logger.info("Inside root function")
   logger.info(f"PostgreSQL Connection String: {os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')}")
   return "Hello world"
 
@app.get("/getUsers")
async def get_users():
    logger.info("Inside function get_users")
    try:
        pool = await create_pool_connection()
        logger.info("Database connection pool created.")
        users = await getUsersDetails(pool)
        logger.info(f"Retrieved users: {users}")
        return users
    except Exception as e:
        logger.error(f"Error in get_users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
 
async def create_pool_connection():
    try:
        logger.info("Creating connection pool")
        db_uri = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
        if not db_uri:
            logger.error("AZURE_POSTGRESQL_CONNECTIONSTRING is not set")
            raise ValueError("AZURE_POSTGRESQL_CONNECTIONSTRING environment variable is not set.")
 
        # Using asyncpg's SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE  # Consider changing to CERT_REQUIRED if you have a valid certificate
 
        logger.info(f"DB URI: {db_uri}")
        pool = await asyncpg.create_pool(dsn=db_uri, ssl=ssl_context, min_size=1, max_size=10)  # Configure the pool
        logger.info("Connection pool created successfully.")
        return pool
    except Exception as e:
        logger.error(f"Error creating pool connection: {e}")
        raise HTTPException(status_code=500, detail="Could not connect to the database")
 
async def getUsersDetails(pool):
    try:
        async with pool.acquire() as connection:
            users = await connection.fetch("SELECT * FROM users")
            return users
    except asyncpg.PostgresError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
 
if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=8000)