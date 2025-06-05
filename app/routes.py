from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .models import Book
from . import db

bp = Blueprint('book', __name__)

# API Routes
@bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([
        {"id": b.id, "title": b.title, "author": b.author, "year": b.year} for b in books
    ])

@bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], year=data['year'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added"}), 201

# UI Routes
@bp.route('/')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)

@bp.route('/add', methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = int(request.form['year'])
        new_book = Book(title=title, author=author, year=year)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('book.home'))
    return render_template('add_book.html')
