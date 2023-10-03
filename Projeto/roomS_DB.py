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
    owner = Column(String, nullable=False)

    def __repr__(self):
        return f"<Room(name='{self.name}', owner='{self.owner}')>"


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    slot_start = Column(String, nullable=False)
    slot_end = Column(String, nullable=False)
    weekday = Column(String, nullable=False)
    room_id = Column(Integer, ForeignKey("room.id"))
    room = relationship("Room", back_populates="schedule")

    def __repr__(self):
        return f"<Schedule(weekday='{self.weekday}, slot_start={self.slot_start}, slot_end={self.slot_end}')>"


Room.schedule = relationship("Schedule", order_by=Schedule.id, back_populates="room")


Base.metadata.create_all(engine)  # Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()


def createRoom(name, owner):
    room = Room(name=name, owner=owner)
    session.add(room)
    session.commit()


def findRoom(name):
    return session.query(Room).filter_by(name=name).first()


def myRooms(owner):
    return session.query(Room).filter_by(owner=owner)


def createSchedule(weekday, slot_start, slot_end, room_id):
    schedule = Schedule(
        weekday=weekday, slot_start=slot_start, slot_end=slot_end, room_id=room_id
    )
    session.add(schedule)
    session.commit()


def deleteSchedule(room_id):
    session.query(Schedule).filter_by(room_id=room_id).delete()
    session.commit()
