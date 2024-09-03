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

# from typing import List
# import asyncpg
# from fastapi import FastAPI, status, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.gzip import GZipMiddleware
# from pydantic import BaseModel
# import os
# import urllib

# # Environment variables for database connection
# # host_server = os.environ.get('host_server')
# # db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port')))
# # database_name = os.environ.get('database_name', 'fastapi')
# # db_username = urllib.parse.quote_plus(str(os.environ.get('db_username')))
# # db_password = urllib.parse.quote_plus(str(os.environ.get('db_password')))


# DATABASE_URL = f'postgresql://azureuser:sevenlake%40123@fitness-db-public.postgres.database.azure.com:5432/postgres?sslmode=require'

# # Initialize FastAPI app
# app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
# app.add_middleware(GZipMiddleware)

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
# async def get_user_function():
#     query = "SELECT * FROM users"
#     print("query",query)
#     print("url",DATABASE_URL)
#     async with app.state.db_pool.acquire() as connection:
#         user = await connection.fetchrow(query)
#     return {"users data",user}


from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import Session, sessionmaker
import os
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
# host_server = os.getenv('PGHOST')
# db_server_port = os.getenv('PGPORT')
# database_name = os.getenv('PGDATABASE')
# db_username = os.getenv('PGUSER')
# db_password = os.getenv('PGPASSWORD')
# ssl_mode = os.getenv('SSL')

# Construct the database URL
DATABASE_URL = f'postgresql://azureuser:sevenlake%40123@fitness-db-public.postgres.database.azure.com:5432/postgres?sslmode=require'

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Define the metadata and users table
metadata = MetaData()
users_table = Table(
    'users', metadata,
    Column('userid', String, primary_key=True),
    Column('username', String),
    Column('mailid', String)
)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define metadata and users table
metadata = MetaData()

users = Table(
    'users', metadata,
    Column('userid', String, primary_key=True, nullable=False),
    Column('username', String),
    Column('mailid', String)
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    print("inside root function")
    return("Hello world")


@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    print("before get db connection")
    try:
        stmt = select(users.c.userid, users.c.username, users.c.mailid)
        result = db.execute(stmt)
        print("result",result)
        users_list = [{"userid": row.userid, "username": row.username, "mailid": row.mailid} for row in result]
        return {"users": users_list}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.on_event("startup")
# async def startup():
#     # Connect to the database at startup
#     metadata.create_all(bind=engine)

# @app.on_event("shutdown")
# async def shutdown():
#     # Optionally close the engine or clean up any resources
#     engine.dispose()

# @app.get("/users")
# async def get_users():
#     # Create a new session
#     session = SessionLocal()
#     try:
#         # Execute a query to select all users
#         query = select([users_table])
#         result = session.execute(query).fetchall()
#         if not result:
#             raise HTTPException(status_code=404, detail="No users found")
#         return {"users": [dict(row) for row in result]}
#     except Exception as e:
#         print(f"Error fetching users: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
#     finally:
#         # Close the session after the query
#         session.close()




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
