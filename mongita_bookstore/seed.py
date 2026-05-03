from mongita import MongitaClientDisk
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = MongitaClientDisk(os.path.join(BASE_DIR, "mongita_data"))

db = client.bookstore

categories_col = db.categories
books_col = db.books

# Reset collections
categories_col.delete_many({})
books_col.delete_many({})

# -----------------------------
# CATEGORIES
# -----------------------------
categories_col.insert_many([
        {"id": 1, "name": "Biographies"},
        {"id": 2, "name": "Learn to Play"},
        {"id": 3, "name": "Music Theory"},
        {"id": 4, "name": "Scores and Charts"}
])

# -----------------------------
# BOOKS
# -----------------------------
books_col.insert_many([
        {
                    "id": 1,
                    "categoryId": 1,
                    "categoryName": "Biographies",
                    "title": "Beethoven",
                    "author": "David Jacobs",
                    "isbn": "13-9780304936588",
                    "price": 9.99,
                    "image": "beethoven.gif",
                    "readNow": 0
        },
        {
                    "id": 2,
                    "categoryId": 1,
                    "categoryName": "Biographies",
                    "title": "Madonna",
                    "author": "Andrew Morton",
                    "isbn": "13-9780312287863",
                    "price": 12.99,
                    "image": "madonna.jpg",
                    "readNow": 1
        },
        {
                    "id": 3,
                    "categoryId": 1,
                    "categoryName": "Biographies",
                    "title": "Clapton: The Autobiography",
                    "author": "Eric Clapton",
                    "isbn": "13-9780767925365",
                    "price": 10.99,
                    "image": "clapton.jpg",
                    "readNow": 1
        },
        {
                    "id": 4,
                    "categoryId": 1,
                    "categoryName": "Biographies",
                    "title": "Music is My Mistress",
                    "author": "Edward Kennedy Ellington",
                    "isbn": "13-9780303608037",
                    "price": 68.99,
                    "image": "ellington.jpg",
                    "readNow": 0
        },
        {
                    "id": 5,
                    "categoryId": 2,
                    "categoryName": "Learn to Play",
                    "title": "Play Piano Today!",
                    "author": "Hal Leonard",
                    "isbn": "13-9780634069321",
                    "price": 19.99,
                    "image": "piano.jpg",
                    "readNow": 1
        },
        {
                    "id": 6,
                    "categoryId": 2,
                    "categoryName": "Learn to Play",
                    "title": "Guitar Basics",
                    "author": "James Longworth",
                    "isbn": "13-9780571538163",
                    "price": 14.99,
                    "image": "guitar.jpg",
                    "readNow": 0
        },
        {
                    "id": 7,
                    "categoryId": 3,
                    "categoryName": "Music Theory",
                    "title": "Music Theory Essentials",
                    "author": "Jason W. Solomon",
                    "isbn": "13-9781423492724",
                    "price": 21.95,
                    "image": "theory.jpg",
                    "readNow": 1
        },
        {
                    "id": 8,
                    "categoryId": 4,
                    "categoryName": "Scores and Charts",
                    "title": "Classical Favorites",
                    "author": "Various",
                    "isbn": "13-9780793512737",
                    "price": 15.99,
                    "image": "scores.jpg",
                    "readNow": 0
        }
])

# Export JSON files
categories = list(categories_col.find())
books = list(books_col.find())

with open(os.path.join(BASE_DIR, "categories.json"), "w") as f:
        json.dump(categories, f, indent=2)

with open(os.path.join(BASE_DIR, "books.json"), "w") as f:
        json.dump(books, f, indent=2)

print("Bookstore Mongita DB seeded and JSON exported.")
