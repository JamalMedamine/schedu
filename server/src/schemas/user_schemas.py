from pydantic import BaseModel

class UserCreate(BaseModel):
    username : str 
    email : str 
    firstName : str
    lastName : str
    phoneNumber : str
    password : str

class UserLogin(BaseModel):
    email : str 
    password : str

class UserloginResponse(BaseModel):
    access_token : str
    refresh_token : str


