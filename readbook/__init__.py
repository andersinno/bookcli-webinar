import click
import pyttsx3

from readbook.book_actions import BookAction
from readbook.settings import Settings
from readbook.models import Base, Book

@click.group()
@click.pass_context
def readbook(ctx):
    ctx.ensure_object(dict)

    settings = Settings()
    Base.metadata.create_all(settings.sql_engine)

    ctx.obj["settings"] = settings
    ctx.obj["session"] = settings.Session()

@readbook.command()
@click.option("-l", "--location", help="Scan a given directory for books")
@click.option("--save", is_flag=True, help="Save the books to database after scanning")
@click.pass_context
def scan_books(ctx, location, save):
    """
    Scan for pdf books in the given directory
    """
    actions = BookAction(book_dir=location, session=ctx.obj["session"])
    actions.print_books()
    if save:
        actions.save_book()

@readbook.command()
@click.pass_context
def show_all_books(ctx):
    """
    Show all books from the database
    """
    actions = BookAction(session=ctx.obj["session"])
    actions.print_books(from_db=True)

@readbook.command()
@click.option("-b", "--book-name", help="Name of the book to read")
@click.pass_context
def read_book_by_name(ctx, book_name):
    """
    Read a book by name from the database
    """
    if not book_name:
        click.echo("Book name must be specified")
        return
    engine = pyttsx3.init()
    actions = BookAction(
        session=ctx.obj["session"],
        speak_engine = engine
    )

    book_to_read = actions.session.query(Book).filter_by(name=book_name).first()
    if not book_to_read:
        click.echo(f"Book with the name {book_name} does not exist")
        return
    actions.read_book(book_to_read)
        
        