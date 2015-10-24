from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:mypass@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime


item_user_table = Table('item_user_association', Base.metadata,
                       Column('users_userid', Integer, ForeignKey('users.userid')),
                       Column('items_itemid', Integer, ForeignKey('items.itemid'))
                       )

class User(Base):
  __tablename__ = "users"
  userid = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  password = Column(String, nullable=False)
  items = relationship("Item", order_by = "Item.itemid", backref = "users")
  userbids = relationship("Bid", order_by = "Bid.bidid", backref="users")

class Item(Base):
  __tablename__ = "items"

  itemid = Column(Integer, primary_key=True)
  itemname = Column(String, nullable=False)
  itemdescription = Column(String)
  user_id = Column(Integer, ForeignKey('users.userid'))
  item_bids = relationship("Bid", order_by = "Bid.bidid", backref="items")
  start_time = Column(DateTime, default=datetime.utcnow)


class Bid(Base):
  __tablename__ = "bids"

  bidid = Column(Integer, primary_key=True)
  price = Column(Integer, nullable=False)
  items_id = Column(Integer, ForeignKey('items.itemid'))
  users_id = Column(Integer, ForeignKey('users.userid'))
  biduser = relationship ("User", order_by = "User.userid", backref = "users")
  biditem = relationship ("Item", order_by = "Item.itemid", backref = "items")

Base.metadata.create_all(engine)