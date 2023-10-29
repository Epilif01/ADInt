from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import datetime
from sqlalchemy.orm import sessionmaker
from os import path

# SLQ access layer initialization
DATABASE_FILE = "roomService.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine(
    "sqlite:///%s" % (DATABASE_FILE), echo=False
)  # echo = True shows all SQL calls

Base = declarative_base()


# Declaration of data
class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    room_id = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Room(name='{self.name}', room_id='{self.room_id}')>"


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    slot_start = Column(String, nullable=False)
    slot_end = Column(String, nullable=False)
    weekday = Column(String, nullable=False)
    name = Column(String, nullable=False)
    course_id = Column(Integer, nullable=True)
    type = Column(String, nullable=False)
    place_id = Column(Integer, ForeignKey("room.room_id"))
    room = relationship("Room", back_populates="schedule")

    def __repr__(self):
        return f"<Schedule(weekday='{self.weekday}, slot_start={self.slot_start}, slot_end={self.slot_end}')>"


Room.schedule = relationship("Schedule", order_by=Schedule.id, back_populates="room")


Base.metadata.create_all(engine)  # Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()


def createRoom(name, room_id):
    room = Room(name=name, room_id=room_id)
    session.add(room)
    session.commit()


def findRoom(room_id):
    return session.query(Room).filter_by(room_id=room_id).first()


def myRooms():
    return session.query(Room).all()


def createSchedule(room_id, data):
    for event in data:
        name = event["title"] if event["type"] == "GENERIC" else event["course"]["name"]
        course_id = None if event["type"] == "GENERIC" else event["course"]["id"]

        schedule = Schedule(
            weekday=event["weekday"],
            slot_start=event["start"],
            slot_end=event["end"],
            place_id=room_id,
            name=name,
            course_id=course_id,
            type=event["type"],
        )
        session.add(schedule)
    session.commit()


def deleteSchedule(room_id):
    session.query(Schedule).filter_by(room_id=room_id).delete()
    session.commit()
