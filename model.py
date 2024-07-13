from pydantic import BaseModel
from typing import Union


# Pydantic model for book data, Pydantic is a data validation and settings management library

class User(BaseModel):
    username: str
    email: str
    disabled: Union[bool, None] = None

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

