from typing import Union, Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

from get_books import get_books 

app = FastAPI()

# class Book(BaseModel):
#     title: str
#     author: str
#     text: Union[str, None] = None
#     summary: Union[str, None] = None

class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str
    url: str
    text: Optional[str] = Field(default=None, index=True)
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


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    populate_books()

def populate_books():
    with Session(engine) as session:
        if session.query(Book).first() is None:
            book_data = get_books()
            for book in book_data:
                new_book = Book(
                    title=book_data[book]['title'],
                    author=book_data[book]['author'],
                    url=book_data[book]['url'])
                session.add(new_book)
            session.commit()

@app.post("/books/", response_model=BookRead)
def create_book(book: BookCreate):
    with Session(engine) as session:
        db_book = Book.model_validate(book)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return book


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
        return book

@app.patch("/books/{book_id}", response_model=BookRead)
def update_book(book_id: int, book: BookUpdate):
    with Session(engine) as session:
        db_book = session.get(Book, book_id)
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        book_data = book.model_dump(exclude_unset=True)
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