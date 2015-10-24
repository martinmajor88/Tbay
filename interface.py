import psycopg2
import sys
import logging
import argparse
import heapq
import random

from tbay import User, Item, Bid, session

def put():
  finished = False
  while not finished:
    newuser = User()
    print "Please enter the name you would like to use for your user name: "
    newuser.username = raw_input()
    print "Please enter the password you would like to associate with this account:"
    newuser.password = raw_input()
    session.add (newuser)
    session.commit()
    print "Would you like to create additional accounts? Y/N: "
    answer = raw_input()
    if answer == "n":
      main()

def item():
  finished = False
  while not finished:
    print "Please enter the user name for the user who would like to enter an item for auction: "
    username = raw_input()
    itemuser = session.query(User).filter(User.username==username).first()
    print "Please enter the name of the item you would llike to put up for auction: "
    newitem = Item()
    newitem.itemname = raw_input()
    print "Enter a description of the item: "
    newitem.itemdescription = raw_input()
    itemuser.items.append(newitem)
    session.commit()
    print "would you like to add additional items? Y/N: "
    answer = raw_input()
    if answer == "n":
      main()

def bid():
  finished = False
  while not finished:
    biduser = raw_input("Please enter the user who wishes to place a bid: ")
    biduser = session.query(User).filter(User.username==biduser).first()
    biditem = raw_input("What item would you like to bid on? ")
    biditem = session.query(Item).filter(Item.itemname==biditem).first()
    print "what is the about of your bid?"
    newbid = Bid(price=int(raw_input()))
    session.add (newbid)
    biduser.userbids.append(newbid)
    biditem.item_bids.append(newbid)
    session.commit()
    print "would you like to bid on another item? Y/N: "
    answer = raw_input()
    if answer == "n":
      main()

def query():
  finished = False
  while not finished:
    print "Please see below for a listing of all items up for auction and their bids:"
    print ""
    results = session.query(User).all()
    for result in results:
      print result.username
      for item in result.items:
        print "item =", item.itemname
      for bids in result.userbids:
        print "bids =", bids.biditem.itemname, ": ", bids.price
    print ""
    maxbid = (session.query(Bid).order_by(Bid.price.desc()).limit(1))
    for maxi in maxbid:
      print "And the highest bid is from:", maxi.biduser.username, "with", maxi.price, "dollars!"
      print "Congratulations", maxi.biduser.username, "you are now the proud owner of a shiny new", bids.biditem.itemname,"!"
    print ""
    print "Would you like to run another query? Y/N?: "
    answer = raw_input()
    if answer == "n":
      main()

def main():
  print ""
  print "Welcome to tBay! Please let us know what you would like to do: "
  print ""
  print "To Create a New User Enter (1)"
  print "To Enter Items For a User to Put Up for Auction Enter (2)"
  print "To Bid on Items up for Auction Enter (3)"
  print "To see items up for Auction and Their Highest Bid Enter (4)"
  print ""
  print "To Quit tBay at any time press the Control and C keys at the same time"
  print ""
  selection = raw_input()
  if selection == "1":
    put()
  elif selection == "2":
    item()
  elif selection == "3":
    bid()
  elif selection == "4":
    query()

if __name__ == "__main__":
  main()