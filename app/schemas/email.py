from pydantic import BaseModel


class EmailRead(BaseModel):
    message: str
    email: str
    nickname: str