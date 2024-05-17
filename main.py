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
        description="The Great Gatsby is a novel by American writer F. Scott Fitzgerald. Set in the Jazz Age on Long Island, the novel depicts narrator Nick Carraway's interactions with mysterious millionaire Jay Gatsby and Gatsby's obsession to reunite with his former lover, Daisy Buchanan. Through Nick's eyes, readers witness Gatsby's lavish parties, his enigmatic nature, and his relentless pursuit of an idealized past. The novel explores themes of wealth, class, love, and the American Dream, ultimately portraying the disillusionment that can come with chasing unattainable dreams.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 1",
        id=0
    ),
    Book(
        name="To Kill a Mockingbird",
        description="To Kill a Mockingbird is a novel by Harper Lee. It follows the story of young Scout Finch and her brother Jem, and their father, Atticus Finch, who defends a black man accused of raping a white woman. Set in the racially charged atmosphere of the American South during the 1930s, the novel addresses complex themes of racial injustice, moral growth, and empathy. Through the innocent eyes of Scout, readers experience the profound impact of prejudice and the importance of standing up for what is right, as Atticus Finch becomes a moral hero in his fight for justice.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 2",
        id=1
    ),
    Book(
        name="1984",
        description="1984 is a dystopian novel by George Orwell. It portrays a totalitarian regime where individuality is suppressed and the government exercises control over every aspect of citizens' lives. The novel follows Winston Smith, a man who secretly yearns for truth and freedom in a society dominated by propaganda and surveillance. Through Winston's rebellion against the oppressive regime, Orwell explores themes of censorship, totalitarianism, and the malleability of reality. 1984 serves as a powerful warning about the dangers of unchecked governmental power and the erosion of individual liberties.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 3",
        id=2
    ),
    Book(
        name="The Catcher in the Rye",
        description="The Catcher in the Rye is a novel by J.D. Salinger. It follows the story of Holden Caulfield, a young man who struggles with alienation and disillusionment. Set in 1950s New York, the novel captures Holden's journey as he grapples with the phoniness of the adult world and seeks authenticity. His narrative voice is characterized by cynicism, yet it reveals deep vulnerability and a desire for connection. The Catcher in the Rye delves into themes of identity, belonging, and the pains of growing up, resonating with readers who feel out of place in society.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 1",
        id=3
    ),
    Book(
        name="Pride and Prejudice",
        description="Pride and Prejudice is a novel by Jane Austen. It follows the story of Elizabeth Bennet, who navigates issues of class, marriage, and morality in early 19th century England. The novel centers on Elizabeth's evolving relationship with the wealthy and aloof Mr. Darcy, highlighting the misunderstandings and societal pressures that complicate their romance. Austen's sharp wit and keen observations of social manners provide a satirical yet affectionate critique of the expectations placed on women and the institution of marriage. Pride and Prejudice remains a timeless exploration of love, pride, and societal expectations.",
        created_at=datetime.now().replace(microsecond=0),
        created_by="User 2",
        id=4
    ),
    Book(
        name="To the Lighthouse",
        description="To the Lighthouse is a novel by Virginia Woolf. It explores themes of loss, time, and the complexities of human relationships through the lens of the Ramsay family's annual visit to a lighthouse. The narrative shifts between the perspectives of various characters, capturing their inner thoughts and emotional landscapes. Woolf's stream-of-consciousness style allows for a deep exploration of personal identity and the passage of time. To the Lighthouse is celebrated for its lyrical prose and its profound insights into the nature of human experience, making it a cornerstone of modernist literature.",
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
