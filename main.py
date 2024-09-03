from fastapi import FastAPI, HTTPException
import asyncpg
import os

app = FastAPI()

DATABASE_URL = "postgresql://azureuser:sevenlake%40123@fitness-db-public.postgres.database.azure.com:5432/postgres?sslmode=require"

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
async def get_Users():
    async with app.state.db_pool.acquire() as connection:
        print("get user funct",DATABASE_URL)
        query = "SELECT * FROM users"
        result = await connection.fetchrow(query)
        if result:
            return dict(result)
        else:
            raise HTTPException(status_code=404, detail="user not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
