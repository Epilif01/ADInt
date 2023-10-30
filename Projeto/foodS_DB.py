from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import datetime
from sqlalchemy.orm import sessionmaker
from os import path

# SLQ access layer initialization
DATABASE_FILE = "foodService.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine(
    "sqlite:///%s" % (DATABASE_FILE), echo=False
)  # echo = True shows all SQL calls

Base = declarative_base()


# Declaration of data
class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    # owner = Column(String, nullable=False)

    def __repr__(self):
        return "<Restaurant(name='%s', room_id='%s')>" % (self.name, self.room_id)


class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True)
    item = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurant.room_id"))
    restaurant = relationship("Restaurant", back_populates="menu")

    def __repr__(self):
        return "<Menu(item='%s')>" % (self.item)


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    review = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurant.room_id"))
    restaurant = relationship("Restaurant", back_populates="review")
    user_id = Column(String, nullable=False)

    def __repr__(self):
        return "<Review(review='%s')>" % (self.review)


Restaurant.menu = relationship("Menu", order_by=Menu.id, back_populates="restaurant")
Restaurant.review = relationship(
    "Review", order_by=Review.id, back_populates="restaurant"
)


Base.metadata.create_all(engine)  # Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()


def createRestaurant(name, room_id):
    restaurant = Restaurant(name=name, room_id=room_id)
    session.add(restaurant)
    session.commit()


def findRestaurant(room_id):
    return session.query(Restaurant).filter_by(room_id=room_id).first()


def myRestaurants():
    return session.query(Restaurant).all()


def createMenu(item, restaurant_id):
    menu = Menu(item=item, restaurant_id=restaurant_id)
    session.add(menu)
    session.commit()


def deleteMenu(restaurant_id):
    session.query(Menu).filter_by(restaurant_id=restaurant_id).delete()
    session.commit()


def showReviews(restaurant_id):
    return session.query(Review).filter_by(restaurant_id=restaurant_id).all()
