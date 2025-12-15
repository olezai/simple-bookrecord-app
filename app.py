from flask import Flask, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')

@app.route('/')
def welcome():
  return 'Welcome to the Book Record App!'

@app.route('/health')
def health_check():
  return jsonify({'status': 'healthy', 'service': 'bookrecord-app'})

@app.route('/add/<title>/<author>')
def add_book(title, author):
  db.insert({'title': title, 'author': author})
  return jsonify({'status': 'successful', 'title': title, 'author': author})

@app.route('/books')
def list_books():
  return jsonify(db.all())

if __name__ == '__main__':
  app.run(debug=True, port=5001)