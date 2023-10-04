from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


# SLQ access layer initialization
DATABASE_FILE = "checkin.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine(
    "sqlite:///%s" % (DATABASE_FILE), echo=False
)  # echo = True shows all SQL calls

Base = declarative_base()


# Declaration of data
class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    place_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    timeofcheckin = Column(Date, nullable=False)
    timeofcheckout = Column(Date, nullable=True)

    def __repr__(self):
        return (
            "<Book(place_id='%s', user_id='%s', timeofcheckin='%s', timeofcheckout='%s')>"
            % (self.place_id, self.user_id, self.timeofcheckin, self.timeofcheckout)
        )


Base.metadata.create_all(engine)  # Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()


def new_checkin(place_id, user_id, timeofcheckin, timeofcheckout):
    book = Book(
        place_id=place_id,
        user_id=user_id,
        timeofcheckin=timeofcheckin,
        timeofcheckout=timeofcheckout,
    )
    session.add(book)
    session.commit()


def checkout(place_id, user_id, timeofcheckout):
    book = (
        session.query(Book)
        .filter_by(place_id=place_id, user_id=user_id, timeofcheckout=None)
        .first()
    )
    if book is None:
        return "No checkin found"
    else:
        book.timeofcheckout = timeofcheckout
        session.commit()
        return "Check out successful"


def getCheckin(user_id):
    book = session.query(Book).filter_by(user_id=user_id, timeofcheckout=None).first()
    if book is None:
        return None
    else:
        return book.place_id
