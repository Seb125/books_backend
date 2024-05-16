from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field


app = FastAPI()

# Allow requests from http://localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic model for book data, Pydantic is a data validation and settings management library
class Book(BaseModel):
    name: str
    description: str
    created_at: datetime
    created_by: str
    id: int


# Beispielbuchdaten
books_data = [
    Book(
        name="The Great Gatsby",
        description="The Great Gatsby is a novel by American writer F. Scott Fitzgerald. Set in the Jazz Age on Long Island, the novel depicts narrator Nick Carraway's interactions with mysterious millionaire Jay Gatsby and Gatsby's obsession to reunite with his former lover, Daisy Buchanan.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 1",
        id=0
    ),
    Book(
        name="To Kill a Mockingbird",
        description="To Kill a Mockingbird is a novel by Harper Lee. It follows the story of young Scout Finch and her brother Jem, and their father, Atticus Finch, who defends a black man accused of raping a white woman.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 2",
        id=1
    ),
    Book(
        name="1984",
        description="1984 is a dystopian novel by George Orwell. It portrays a totalitarian regime where individuality is suppressed and the government exercises control over every aspect of citizens' lives.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 3",
        id=2
    ),
    Book(
        name="The Catcher in the Rye",
        description="The Catcher in the Rye is a novel by J.D. Salinger. It follows the story of Holden Caulfield, a young man who struggles with alienation and disillusionment.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 1",
        id=3
    ),
    Book(
        name="Pride and Prejudice",
        description="Pride and Prejudice is a novel by Jane Austen. It follows the story of Elizabeth Bennet, who navigates issues of class, marriage, and morality in early 19th century England.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 2",
        id=4
    ),
    Book(
        name="To the Lighthouse",
        description="To the Lighthouse is a novel by Virginia Woolf. It explores themes of loss, time, and the complexities of human relationships through the lens of the Ramsay family's annual visit to a lighthouse.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 3",
        id=5
    )
]


@app.get('/books')
async def get_books():
    return books_data


@app.put('/books')
async def update_book(updated_book: Book):
    try:
        # Update the book in the books_data list
        for index, book in enumerate(books_data):
            if book.id == updated_book.id:
                # Update the book at the found index
                books_data[index] = updated_book
        return {"message": "Book with ID {book_id} updated successfully"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
