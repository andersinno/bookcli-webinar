import os
from tabulate import tabulate
import click
import pdftotext

from readbook.models import Book

class BookAction:
    def __init__(self, book_dir=None, session=None, speak_engine=None):
        self.book_dir = book_dir
        self.session = session
        self.speak_engine = speak_engine

    def print_books(self, from_db=False):
        """
        Print to the console a table of the books from 
        a directory or from the database
        """
        if from_db:
            books, headers = self.show_book_from_db()
        else:
            books, headers = self.scan_books()
        click.echo(tabulate(books, headers, tablefmt="github"))

    def scan_books(self):
        """
        Scan a directory for pdf books.

        Returns: a tuple of (books, headers)
            - books is a nested list of lists (2D array) [["", "book name", "book path"],...]
            - headers is a list of header strings : ["", "Book name", "Book Path"]
        """
        pdfbooks = os.listdir(self.book_dir)
        headers = ["", "Book name", "Book path"]
        books = []

        for book in pdfbooks:
            book_name = book.split(".pdf")[0]
            book_path = os.path.join(self.book_dir, book)
            books.append(["", book_name, book_path])

        return books, headers

    def save_book(self):
        """
        Save the books to the database
        """
        if not self.session:
            raise Exception("SQLAlchemy session is missing")

        books, _ = self.scan_books()
        book_query = self.session.query(Book)
        book_to_store = []
        for book in books:
            # book = ["", book name, book path]
            if not book_query.filter_by(name=book[1]).count():
                book_to_store.append(
                    Book(name=book[1], book_path=book[2])
                )
        if not book_to_store:
            click.echo("No new books")
            return
        self.session.add_all(book_to_store)
        self.session.commit()
        click.echo(f"{len(book_to_store)} has been saved to database")

    def show_book_from_db(self):
        """
        Show all books available in the database
        """
        all_books = self.session.query(Book).all()
        headers = ["ID", "Book name", "Book path"]
        books = [[book.id, book.name, book.book_path] for book in all_books]

        return books, headers

    def read_book(self, book):
        """
        Use pyttsx engine to read a given book
        :book param: an object of Book model class
        """
        if not self.speak_engine:
            raise Exception("Speech to text engine is missing")

        with open(book.book_path, "rb") as book_file:
            pages = pdftotext.PDF(book_file)

        for _, page in enumerate(pages):
            self.speak_engine.say(page)
            self.speak_engine.runAndWait()