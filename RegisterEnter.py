from pydantic import  BaseModel
class RegisterEnter(BaseModel):
    username: str
    password: str
