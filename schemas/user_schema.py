from pydantic import BaseModel, Field


class User(BaseModel):
    login: str = Field(min_length=4, max_length=70, default="user_login")
    passwd: str = Field(min_length=4, max_length=70, default="user_passwd")