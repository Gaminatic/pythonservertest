from pydantic import BaseModel

class Signup(BaseModel):
    mailid : str
    mobileno:str
    username:str
    password:str

class Signin(BaseModel):
    mailid : str
    password:str   

class SetLevel(BaseModel):
    counts : int
    typeid :str   

class Activities(BaseModel):
    name : str

class UpdateActivities(BaseModel):
    id : str
    name : str

class DltActivities(BaseModel):
    id : str

class eventLogs(BaseModel):
    eid:str
    counts : int
    
class Sigin(BaseModel):
    mailid : str
    password : str    