from flask import Blueprint

bookbp = Blueprint("book",__name__)
@bookbp.route("/")
def index():
    return "book"

@bookbp.route("/bookstudy")
def bookstudy():
    return "bookstudy"