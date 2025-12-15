from flask import Flask, render_template, request, redirect, url_for, flash
import json
from pathlib import Path
import os

app = Flask(__name__)
# In production, set a secure secret key via environment variable:
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "changeit")

BOOKS_FILE = Path(__file__).parent / "db.json"

# replace the existing load_books and save_books with this version

def load_books():
    """
    Load and return a list of books. Handles these cases:
    - missing file -> []
    - file contains a JSON list -> return it
    - file contains a JSON object with "books": [...] -> return that list
    - file contains a JSON object representing a single book -> return [obj]
    - any parse error -> []
    """
    if not BOOKS_FILE.exists():
        return []
    try:
        data = json.loads(BOOKS_FILE.read_text(encoding="utf-8") or "[]")
    except Exception:
        return []

    # Normalize to list
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # common pattern: { "books": [ ... ] }
        books_list = data.get("books")
        if isinstance(books_list, list):
            return books_list
        # otherwise wrap single object into a list
        return [data]
    # unexpected type -> return empty list
    return []

def save_books(books):
    """
    Save books to the books file. Ensures a JSON list is written.
    If a single dict is passed, wrap it into a list.
    """
    if isinstance(books, dict):
        books = [books]
    if not isinstance(books, list):
        # best-effort conversion
        books = list(books)
    BOOKS_FILE.write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")

@app.route("/")
def index():
    return redirect(url_for("books"))

@app.route("/books")
def books():
    books = load_books()
    return render_template("books.html", books=books)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    if not title or not author:
        flash("Please enter both title and author.", "error")
        return redirect(url_for("books"))
    books = load_books()
    books.append({"title": title, "author": author})
    save_books(books)
    flash("Book added.", "success")
    return redirect(url_for("books"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)