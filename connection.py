import asyncio
import logging
import os
from urllib.parse import quote_plus
import asyncpg
from dotenv import load_dotenv

load_dotenv()

# db_params = {
#     "database": os.getenv('PGDATABASE'),
#     "user": os.getenv('PGUSER'),
#     "password": os.getenv('PGPASSWORD'),
#     "host": os.getenv('PGHOST'),
#     "port": os.getenv('PGPORT'),
#     # "sslmode": os.getenv('SSL')  
# }

# # ssl_mode = os.getenv('SSL') == 'true'
# # ssl_context = ssl.create_default_context() if ssl_mode else None
# db_url = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
# print("db_url",db_url)
# pool = None

# async def create_pool():
#     global pool
#     if pool is None:
#         pool = await asyncpg.create_pool(db_url,timeout=30)
#     return pool

# async def acquire_connection():
#     if pool is None:
#         await create_pool()
#     return await pool.acquire()

# async def release_connection(conn):
#     await pool.release(conn)

# async def close_pool():
#     global pool
#     if pool is not None:
#         try:
#             await asyncio.wait_for(pool.close(), timeout=10.0)
#         except asyncio.TimeoutError:
#             print("Pool close operation timed out.")
#         pool = None


# async def with_connection(func, *args, **kwargs):
#     conn = await acquire_connection()
#     try:
#         # print(f"Connection type: {type(conn)}")
#         return await func(*args, conn=conn, **kwargs)  
#     finally:
#         await release_connection(conn)


# async def getUsersDetails(conn):
#     try:
#         result = await conn.fetchrow('SELECT * FROM users')
#         return result   
    
#     except Exception as e:
#         raise e
    

# async def create_pool_connection():
#     print("inside connection")
#     db_uri = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
#     print(f"DB URI: {db_uri}") 
#     return await asyncpg.create_pool(db_uri)


# async def getUsersDetails(pool:asyncpg.pool):
#     async with pool.acquire() as conn:
#         try:
#             users = await conn.fetchrow("SELECT * FROM users")
#             return users

#         except asyncpg.PostgresError as e:
#             raise e   


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
            # db_params = {
            #     "database": os.getenv('PGDATABASE'),
            #     "user": os.getenv('PGUSER'),
            #     "password": os.getenv('PGPASSWORD'),
            #     "host": os.getenv('PGHOST'),
            #     "port": os.getenv('PGPORT')
            # }
            db_uri = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
            print("url",db_uri)
            self._pool = await asyncpg.create_pool(dsn=db_uri,timeout = 60)

            # self._pool = await asyncpg.create_pool(**db_params)
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
