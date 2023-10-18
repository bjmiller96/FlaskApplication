from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import uuid
import secrets

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(50), nullable = True, default = '')
    last_name = db.Column(db.String(50), nullable = True, default = '')
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True, default = '')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    g_auth_verify = db.Column(db.Boolean, default = False)

    def __init__(self, email, password, id = '', first_name = '', last_name = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_pass(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_pass(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def __repr__(self):
        return f"{self.email} has been added to the Digital Library."

class Book(db.Model):
    id = db.Column(db.String, primary_key = True)
    isbn = db.Column(db.String(20))
    title = db.Column(db.String(150))
    author = db.Column(db.String(150))
    pages = db.Column(db.Integer)
    cover_type = db.Column(db.String(20), nullable = True, default = '')
    date_published = db.Column(db.Date, nullable = True, default = '')
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, isbn, title, author, pages, user_token, cover_type = '', date_published = '', id = ''):
        self.id = self.set_id()
        self.isbn = isbn
        self.title = title
        self.author = author
        self.pages = pages
        self.cover_type = cover_type
        self.date_published = date_published
        self.user_token = user_token

    def __repr__(self):
        return f"The book '{self.title}' has been added to the Digital Library"
    
    def set_id(self):
        return secrets.token_urlsafe()
    
class BookSchema(ma.Schema):
    class Meta:
        fields = ['id', 'isbn', 'title', 'author', 'pages', 'cover_type', 'date_published']

book_schema = BookSchema()
books_schema = BookSchema(many = True)