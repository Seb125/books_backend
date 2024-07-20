from pydantic import BaseModel, Field
from typing import Union, List


# Pydantic model for book data, Pydantic is a data validation and settings management library

class User(BaseModel):
    username: str
    email: str
    disabled: Union[bool, None] = False
    books: List[str] = Field(default_factory=list)

class UserNew(User):
    password: str

class UserInDB(User):
    hashed_password: str

class Book(BaseModel):
    name: str
    description: str
    created_at: str
    created_by: str
    favorite: bool


class BookInDB(Book):
    id:str

class Message(BaseModel):
    role: str
    msg: str
    time: str

class Request(BaseModel):
    message: List[Message]


