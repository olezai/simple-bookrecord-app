from flask import Flask, render_template, request, redirect, url_for, flash
import json
from pathlib import Path
import os

app = Flask(__name__)
# In production, set a secure secret key via environment variable:
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "changeit")

BOOKS_FILE = Path(__file__).parent / "db.json"

def load_books():
    if not BOOKS_FILE.exists():
        return []
    try:
        return json.loads(BOOKS_FILE.read_text(encoding="utf-8") or "[]")
    except Exception:
        return []

def save_books(books):
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