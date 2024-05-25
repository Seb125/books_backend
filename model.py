from pydantic import BaseModel, Field



# Pydantic model for book data, Pydantic is a data validation and settings management library
class Book(BaseModel):
    name: str
    description: str
    created_at: str
    created_by: str


class BookInDB(Book):
    id:str

