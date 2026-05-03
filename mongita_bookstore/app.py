from flask import Flask, render_template, request, redirect, url_for
from mongita import MongitaClientDisk
import os
import json

app = Flask(__name__)

# ------------------------------------------
# Mongita Setup (local embedded NoSQL DB)
# ------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = MongitaClientDisk(os.path.join(BASE_DIR, "mongita_data"))

db = client.bookstore
categories_col = db.categories
books_col = db.books


# ------------------------------------------
# Helper Functions
# ------------------------------------------
def get_categories():
        categories = list(categories_col.find())
        return sorted(categories, key=lambda c: c["name"])


def get_next_book_id():
        books = list(books_col.find())
        if not books:
                    return 1
                return max(book["id"] for book in books) + 1


# ------------------------------------------
# HOME PAGE - list categories
# ------------------------------------------
@app.route("/", methods=["GET"])
def home():
        categories = get_categories()
    return render_template("index.html", categories=categories)


# ------------------------------------------
# READ - list all books
# ------------------------------------------
@app.route("/read", methods=["GET"])
def read():
        categories = get_categories()
    books = list(books_col.find())
    books = sorted(books, key=lambda b: b["title"])
    return render_template("read.html", books=books, categories=categories)


# ------------------------------------------
# CREATE - show form
# ------------------------------------------
@app.route("/create", methods=["GET"])
def create():
        categories = get_categories()
    return render_template("create.html", categories=categories)


# ------------------------------------------
# CREATE POST - insert book
# ------------------------------------------
@app.route("/create_post", methods=["POST"])
def create_post():
        title = request.form.get("title")
    author = request.form.get("author")
    isbn = request.form.get("isbn")
    price = request.form.get("price", type=float)
    image = request.form.get("image")
    category_id = request.form.get("categoryId", type=int)
    read_now = request.form.get("readNow", type=int, default=0)

    selected_category = categories_col.find_one({"id": category_id})
    category_name = selected_category["name"] if selected_category else ""

    new_book = {
                "id": get_next_book_id(),
                "categoryId": category_id,
                "categoryName": category_name,
                "title": title,
                "author": author,
                "isbn": isbn,
                "price": price,
                "image": image,
                "readNow": read_now
    }

    books_col.insert_one(new_book)

    # Export JSON files after insert
    export_json()

    return redirect(url_for("read"))


# ------------------------------------------
# EDIT - show pre-filled form
# ------------------------------------------
@app.route("/edit/<int:book_id>", methods=["GET"])
def edit(book_id):
        categories = get_categories()
    book = books_col.find_one({"id": book_id})
    if not book:
                return render_template("error.html", error="Book not found"), 404
            return render_template("edit.html", book=book, categories=categories)


# ------------------------------------------
# EDIT POST - update book
# ------------------------------------------
@app.route("/edit_post/<int:book_id>", methods=["POST"])
def edit_post(book_id):
        title = request.form.get("title")
    author = request.form.get("author")
    isbn = request.form.get("isbn")
    price = request.form.get("price", type=float)
    image = request.form.get("image")
    category_id = request.form.get("categoryId", type=int)
    read_now = request.form.get("readNow", type=int, default=0)

    selected_category = categories_col.find_one({"id": category_id})
    category_name = selected_category["name"] if selected_category else ""

    books_col.replace_one(
                {"id": book_id},
                {
                                "id": book_id,
                                "categoryId": category_id,
                                "categoryName": category_name,
                                "title": title,
                                "author": author,
                                "isbn": isbn,
                                "price": price,
                                "image": image,
                                "readNow": read_now
                }
    )

    # Export JSON files after update
    export_json()

    return redirect(url_for("read"))


# ------------------------------------------
# DELETE - delete book
# ------------------------------------------
@app.route("/delete/<int:book_id>", methods=["GET"])
def delete(book_id):
        books_col.delete_one({"id": book_id})

    # Export JSON files after delete
    export_json()

    return redirect(url_for("read"))


# ------------------------------------------
# JSON Export Helper
# ------------------------------------------
def export_json():
        categories = list(categories_col.find())
    books = list(books_col.find())

    with open(os.path.join(BASE_DIR, "categories.json"), "w") as f:
                json.dump(categories, f, indent=2)

    with open(os.path.join(BASE_DIR, "books.json"), "w") as f:
                json.dump(books, f, indent=2)


# ------------------------------------------
# ERRORS
# ------------------------------------------
@app.errorhandler(Exception)
def handle_error(e):
        return render_template("error.html", error=e), 500


# ------------------------------------------
# RUN APP
# ------------------------------------------
if __name__ == "__main__":
        port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
