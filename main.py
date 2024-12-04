import os
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import JSON

from data_processing.get_books import fetch_books, process_books
from data_processing.get_text import write_text_to_book

app = FastAPI()
os.environ["PYTHONBREAKPOINT"] = "ipdb.set_trace"

# class Book(BaseModel):
#     title: str
#     author: str
#     text: Union[str, None] = None
#     summary: Union[str, None] = None


class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str
    url: str
    text: Optional[dict] = Field(sa_type=JSON)
    summary: Optional[str] = Field(default=None, index=True)


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int


class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    text: Optional[str] = None
    summary: Optional[str] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Uncomment this to empty the database (after schema changes etc.)
# SQLModel.metadata.drop_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    populate_books()


def populate_books():
    with Session(engine) as session:
        if session.query(Book).first() is None:
            book_data = process_books(fetch_books())
            for book in book_data:
                new_book = Book(
                    title=book_data[book]["title"],
                    author=book_data[book]["author"],
                    url=book_data[book]["url"],
                )
                session.add(new_book)
        first_book = session.query(Book).first()
        if first_book is not None and first_book.text is None:
            books = session.exec(select(Book)).all()
            # Process for saving each book to its own file
            # for book in books:
            #     filename = f"./books/{book.id}_{book.title.replace(' ', '_')}.txt"
            #     book.text = write_text_to_file(book.url, filename)

            for book in books:
                print(f"Getting text for {book.title}.")
                book.text = write_text_to_book(book.url)

        session.commit()


@app.get("/")
def root():
    return {"Summarize": "books"}


@app.post("/books/", response_model=BookRead)
def create_book(book: BookCreate):
    with Session(engine) as session:
        db_book = Book.model_validate(book)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book


@app.get("/books/", response_model=List[Book])
def read_books():
    with Session(engine) as session:
        books = session.exec(select(Book)).all()
        return books


@app.get("/books/{book_id}", response_model=BookRead)
def read_book(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        breakpoint()
        return book


@app.patch("/books/{book_id}", response_model=BookRead)
def update_book(book_id: int, book: BookUpdate):
    with Session(engine) as session:
        db_book = session.get(Book, book_id)
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        book_data = book.dict(exclude_unset=True)
        for key, value in book_data.items():
            setattr(db_book, key, value)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        session.delete(book)
        session.commit()
        return {"ok": True}
