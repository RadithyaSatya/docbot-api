from pydantic import BaseModel


class UserCreate(BaseModel):
    username:str
    email:str
    password:str
    
    class Config:
        json_schema_extra={
            "example":{
                "username":"docbot",
                "email":"docbot@gmail.com",
                "password":"password"
            }
        }

class UserLogin(BaseModel):
    username:str
    password:str

    class Config:
        json_schema_extra={
            "example":{
                "username":"docbot",
                "password":"password"
            }
        }