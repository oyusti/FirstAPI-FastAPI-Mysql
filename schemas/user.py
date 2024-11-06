
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(default=None)
    name:str
    email: str
    password: str
    
class UserResponse(BaseModel):
    user: User
    msg: str    
    
class UserMsgStr(BaseModel):
    msg: str