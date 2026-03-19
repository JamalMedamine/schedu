from pydantic import BaseModel

class UserCreate(BaseModel):
    username : str 
    email : str 
    firstName : str
    lastName : str
    phoneNumber : str
    password : str


