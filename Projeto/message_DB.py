from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SLQ access layer initialization
DATABASE_FILE = "message.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    sender = Column(String, nullable=False)
    message = Column(String, nullable=False)
    destination = Column(String, nullable=False)

    def __repr__(self):
        return "<Message(sender='%s', message='%s', destination='%s')>" % (
                                self.sender, self.message, self.destination)

Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()

def new_message(sender, message, destination):
    message = Message(sender=sender, message=message, destination=destination)
    session.add(message)
    session.commit()

def messages_sent(sender):
    messages = session.query(Message).filter_by(sender=sender).all()
    return messages

def messages_received(destination):
    messages = session.query(Message).filter_by(destination=destination).all()
    return messages