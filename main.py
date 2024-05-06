from fastapi import FastAPI
import random
from datetime import datetime
from pydantic import BaseModel





app = FastAPI()


@app.get('/')
async def root():
    return {'example': 'This is an example 2'}

@app.get('/random')
async def get_random():
    rn:int = random.randint(0, 100)
    return {'number': rn}
                            
@app.get('/random/{limit}')
async def get_random(limit: int):
    rn:int = random.randint(0, limit)
    return {'number': rn}


class Book(BaseModel):
    name: str
    description: str
    created_at: datetime
    created_by: str

# Beispielbuchdaten
books_data = [
    Book(name="Book 1", description="Description of Book 1", created_at=datetime.now(), created_by="User 1"),
    Book(name="Book 2", description="Description of Book 2", created_at=datetime.now(), created_by="User 2"),
    Book(name="Book 3", description="Description of Book 3", created_at=datetime.now(), created_by="User 3")
]

@app.get('/books')
async def get_books():
    return books_data

@app.get('/books/{book_id}')
async def get_book(book_id: int):
    if book_id < len(books_data):
        return books_data[book_id]
    else:
        return {"message": "Book not found"}

@app.post('/books')
async def create_book(book: Book):
    books_data.append(book)
    return {"message": "Book created successfully"}
