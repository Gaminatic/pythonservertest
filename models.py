from pydantic import BaseModel


class Signup(BaseModel):
    mailid : str
    mobileno:str
    username:str
    password:str