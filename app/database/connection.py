import asyncio
import json
import logging
import os
from urllib.parse import quote_plus
import asyncpg
from dotenv import load_dotenv

load_dotenv()

db_params = {
    "database": os.getenv('PGDATABASE'),
    "user": os.getenv('PGUSER'),
    "password": os.getenv('PGPASSWORD'),
    "host": os.getenv('PGHOST'),
    "port": os.getenv('PGPORT'),
    # "sslmode": os.getenv('SSL')  
}

# ssl_mode = os.getenv('SSL') == 'true'
# ssl_context = ssl.create_default_context() if ssl_mode else None
db_url = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
print("db_url",db_url)
pool = None

async def create_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(db_url,timeout=30)
    return pool

async def acquire_connection():
    if pool is None:
        await create_pool()
    return await pool.acquire()

async def release_connection(conn):
    await pool.release(conn)

async def close_pool():
    global pool
    if pool is not None:
        try:
            await asyncio.wait_for(pool.close(), timeout=10.0)
        except asyncio.TimeoutError:
            print("Pool close operation timed out.")
        pool = None


async def with_connection(func, *args, **kwargs):
    conn = await acquire_connection()
    try:
        # print(f"Connection type: {type(conn)}")
        return await func(*args, conn=conn, **kwargs)  
    finally:
        await release_connection(conn)



async def login_user(email, password,conn):
    try:
        result = await conn.fetchrow('SELECT * FROM login($1, $2)', email, password)
        if result:
            return json.loads(result['login'])
        return None
    except Exception as e:
        raise e


async def signup(mailid, mobileno, username, password, conn):
    try:
        result = await conn.fetchrow('SELECT * FROM create_user($1, $2, $3, $4)', mailid, mobileno, username, password)
        return result
    except Exception as e:
        raise e













