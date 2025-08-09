from pydantic import  BaseModel
class ChatGptEntranceDto(BaseModel):
    message: str
