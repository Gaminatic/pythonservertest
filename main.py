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
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from connection import db_url, with_connection,getUsersDetails

from connection import acquire_connection, close_pool

app = FastAPI()
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("database",os.getenv("PGDATABASE"))
    print("db url",db_url)
    await acquire_connection()
    print(asyncpg.__version__)
    try:
        yield
    finally:
        await close_pool()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
   print("Inside function")
   return("Hello world")


@app.get("/getUsers")
async def get_users():
   print("Inside function get_users")
   users = await with_connection(getUsersDetails)
   return users



if __name__ == '__main__':
   uvicorn.run(app,host="0.0.0.0",port=8000)
