from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List
from model import Book
from model import BookInDB
import json
from bson import ObjectId


# Read the JSON file
with open('books.json', 'r') as file:
    books_data = json.load(file)


app = FastAPI()

# MongoDB connection string
MONGO_DETAILS = "mongodb://localhost:27017"

# Database client
client = AsyncIOMotorClient(MONGO_DETAILS)

# Database and collection
database = client.test_db
collection = database.books


@app.post("/items/", response_model=BookInDB)
async def create_item(book: Book):
    book_dict = book.dict()
    result = await collection.insert_one(book_dict)
    book_in_db = await collection.find_one({"_id": result.inserted_id})
    book_in_db["id"] = str(book_in_db["_id"])
    del book_in_db["_id"]
    return book_in_db

# Allow requests from http://localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get('/insert-books')
async def insert_books():
    for index, book in enumerate(books_data):
        result = await collection.insert_one(book)


@app.get('/books', response_model=List[BookInDB])
async def get_books():
    books = []
    async for book in collection.find():
        book_in_db = book.copy()
        book_in_db["id"] = str(book_in_db["_id"])
        del book_in_db["_id"]
        books.append(BookInDB(**book_in_db))
    return books


@app.put('/books')
async def update_book(updated_book: BookInDB):
    try:
        # Convert the BookInDB object to a dictionary
        updated_book_dict = updated_book.dict()
        
        # Extract the id from the dictionary and remove it to avoid updating the id field
        book_id = ObjectId(updated_book_dict.pop('id', None))
        print(book_id)
        result = await collection.update_one({'_id': book_id}, {"$set": updated_book_dict})
        print(result)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete('/books/{bookId}')
async def delete_book(bookId: str):
    try:

        book_id = ObjectId(bookId)
        result = await collection.delete_one({'_id': book_id})

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete('/books/{bookId}')
async def delete_book(bookId: int):
    try:
        # Update the book in the books_data list
        for index, book in enumerate(books_data):
            if book.id == bookId:
                # Delete the book at the found index
                del books_data[index]
        return {"message": "Book with ID {book_id} deleted successfully"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")