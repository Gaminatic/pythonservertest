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
    

async def adminSignup(mailid, mobileno, username, password, conn):
    try:
        result = await conn.fetchrow('SELECT * FROM create_admin($1, $2, $3, $4)', mailid, mobileno, username, password)
        return result
    except Exception as e:
        raise e

async def getActivities(adminid,conn):
    try:
        result = await conn.fetchrow('SELECT * FROM get_activities($1)',adminid)
        if result:
            activities = json.loads(result['get_activities'])
            return activities
        return None    
    
    except Exception as e:
        raise e

async def createActivities(adminid,name,conn):
    try:
        result = await conn.fetchrow('SELECT * FROM create_or_update_activities($1,$2)',adminid,name)
        return result
        # return None    
    except Exception as e:
        raise e
    

async def updateactivities(adminid,typeid,name,conn):
    try:
        result = await conn.fetchrow('SELECT * FROM update_activity_by_id($1,$2,$3)',adminid,typeid,name)
        return result 
    except Exception as e:
        raise e


async def deleteActivities(adminid,typeid,conn):
    try:
        result = await conn.fetchrow('SELECT * FROM delete_activities($1,$2)',adminid,typeid)
        return result
    except Exception as e:
        raise e
    

async def setlevel(count,userid,typeid,conn):
    try:
        result = await conn.fetchrow('SELECT * FROM update_arrangegroup4($1,$2,$3)', count,userid,typeid)
        print("result",result)
        if result:
            level_data = json.loads(result['update_arrangegroup4'])
            return level_data
        return None
    except Exception as e:
        raise e

async def getlevel(userid,conn):
    try:
        result = await conn.fetchrow('SELECT * FROM get_user_level($1)', userid)
        if result:
            level_data = json.loads(result['get_user_level'])
            return level_data
        return None
    except Exception as e:
        raise e
    
async def inserteventCounts(userid,eventid,counts,conn):
    try:
        result = await conn.fetchrow('SELECT insert_or_update_eventlog1($1, $2, $3)', userid,eventid,counts)
        if result:
            event = result['insert_or_update_eventlog1']
            return event
    except Exception as e:
        raise e

async def geteventList(userid, conn):
    try:
        result = await conn.fetchrow('SELECT get_events_list($1)', userid)
        if result:
            eventlist = json.loads(result['get_events_list'])
            return eventlist
        return None
    except Exception as e:
        raise e
    
async def eventMembers(eid,userid,conn):
    try:
        result = await conn.fetchrow('SELECT * FROM g($1,$2)',eid,userid)
        if result:
            emembers = json.loads(result['g'])
            return emembers
        return None
    except Exception as e:
        raise e

async def scoreBoard(userid,conn):
    try:
        result = await conn.fetchrow('SELECT * FROM get_completed_event_members1($1)',userid)
        print("result",result)
        if result:
            score_board = json.loads(result['get_completed_event_members1'])
            return score_board
        return None
    except Exception as e:
        raise e







