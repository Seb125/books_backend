from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import gridfs





# MongoDB connection string
MONGO_DETAILS = "mongodb://books-mongodb-1:27017" 


# Database client
client = AsyncIOMotorClient(MONGO_DETAILS)

# Database and collection
database = client.test_db
collection_books = database.books
collection_users = database.users

# Synchronous client for GridFS
# GridFS for asynchronous operations


