import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestApp(unittest.TestCase):

    def test_create_item(self):
        # Test creating a new book item
        new_book = {"name": "Test Book", "description": "Test Author"}
        response = client.post("/items/", json=new_book)
        self.assertEqual(response.status_code, 200)
        created_book = response.json()
        self.assertTrue("id" in created_book)
        self.assertEqual(created_book["title"], new_book["title"])
        self.assertEqual(created_book["author"], new_book["author"])

    def test_get_books(self):
        # Test retrieving all books
        response = client.get("/books")
        self.assertEqual(response.status_code, 200)
        books = response.json()
        self.assertIsInstance(books, list)

    def test_update_book(self):
        # Test updating an existing book
        updated_book = {"id": "1", "title": "Updated Title", "author": "Updated Author"}
        response = client.put("/books", json=updated_book)
        self.assertEqual(response.status_code, 200)
        updated_book_response = response.json()
        self.assertEqual(updated_book_response["title"], updated_book["title"])
        self.assertEqual(updated_book_response["author"], updated_book["author"])

    def test_delete_book(self):
        # Test deleting an existing book
        book_id_to_delete = "existing_book_id"
        response = client.delete(f"/books/{book_id_to_delete}")
        self.assertEqual(response.status_code, 200)
        deletion_response = response.json()
        self.assertEqual(deletion_response["message"], f"Book with ID {book_id_to_delete} deleted successfully")

if __name__ == '__main__':
    unittest.main()
