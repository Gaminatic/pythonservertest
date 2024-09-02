import asyncio
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


# async def getUsersDetails(conn):
#     try:
#         result = await conn.fetchrow('SELECT * FROM users')
#         return result   
    
#     except Exception as e:
#         raise e
    

async def create_pool_connection():
    print("inside connection")
    db_uri = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
    print(f"DB URI: {db_uri}") 
    return await asyncpg.create_pool(db_uri)




# from sqlmodel import create_engine

# logger = logging.getLogger("app")
# logger.setLevel(logging.INFO)

# sql_url = ""
# if os.getenv("WEBSITE_HOSTNAME"):
#     logger.info("Connecting to Azure PostgreSQL Flexible server based on AZURE_POSTGRESQL_CONNECTIONSTRING...")
#     env_connection_string = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
#     if env_connection_string is None:
#         logger.info("Missing environment variable AZURE_POSTGRESQL_CONNECTIONSTRING")
#     else:
#         # Parse the connection string
#         details = dict(item.split('=') for item in env_connection_string.split())

#         # Properly format the URL for SQLAlchemy
#         sql_url = (
#             f"postgresql://{quote_plus(details['user'])}:{quote_plus(details['password'])}"
#             f"@{details['host']}:{details['port']}/{details['dbname']}?sslmode={details['sslmode']}"
#         )

# else:
#     logger.info("Connecting to local PostgreSQL server based on .env file...")
#     load_dotenv()
#     POSTGRES_USERNAME = os.environ.get("PGUSER")
#     POSTGRES_PASSWORD = os.environ.get("PGPASSWORD")
#     POSTGRES_HOST = os.environ.get("PGHOST")
#     POSTGRES_DATABASE = os.environ.get("PGDATABASE")
#     POSTGRES_PORT = os.environ.get("PGPORT", 5432)

#     sql_url = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

# engine = create_engine(sql_url)


async def getUsersDetails(pool:asyncpg.pool):
    async with pool.acquire() as conn:
        try:
            users = await conn.fetchrow("SELECT * FROM users")
            return users

        except asyncpg.PostgresError as e:
            raise e   

