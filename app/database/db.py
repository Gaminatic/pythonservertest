import json


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