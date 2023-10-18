from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix = '/api')

# Create a book
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    pages = request.json['pages']
    cover_type = request.json['cover_type']
    date_published = request.json['date_published']
    user_token = current_user_token.token
    
    print(f"BIG TESTER: {current_user_token.token}")

    book = Book(isbn, title, author, pages, user_token = user_token, cover_type = cover_type, date_published = date_published)
    db.session.add(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# Retrieve a single book
@api.route('/books/<id>', methods = ['GET'])
@token_required
def retrieve_book(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({'message': 'vaild token required'}), 401
    
# Retrieve all books
@api.route('/books', methods = ['GET'])
@token_required
def retrieve_books(current_user_token):
    owner = current_user_token.token
    books = Book.query.filter_by(user_token = owner).all()
    response = books_schema.dump(books)
    return jsonify(response)

# Update a book
@api.route('/books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.isbn = request.json['isbn']
    book.title = request.json['title']
    book.author = request.json['author']
    book.pages = request.json['pages']
    book.cover_type = request.json['cover_type']
    book.date_published = request.json['date_published']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# Delete a book
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)