from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from db import db
from models import Book
from schemas import BookSchema

blp = Blueprint("Books", "books", url_prefix="/books", description="Operations on books")

@blp.route("/")
class BookList(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        """List all books"""
        return Book.query.all()

    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, new_data):
        """Create a new book"""
        book = Book(**new_data)
        db.session.add(book)
        db.session.commit()
        return book

@blp.route("/<int:book_id>")
class BookDetail(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        """Get book by ID"""
        book = Book.query.get_or_404(book_id)
        return book

    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def put(self, updated_data, book_id):
        """Update an existing book"""
        book = Book.query.get_or_404(book_id)
        book.title = updated_data["title"]
        book.author = updated_data["author"]
        book.description = updated_data.get("description")
        db.session.commit()
        return book

    def delete(self, book_id):
        """Delete a book"""
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted"}, 204
