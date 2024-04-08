from models.bid_db import Bid_Items, engine
from sqlalchemy.orm import sessionmaker

# Function for read bid database
def read_bid_db ():
    Session = sessionmaker (bind=engine)
    session = Session()
    query = session.query (Bid_Items).all()
    data = []
    for items in query:
        item = []
        item.append (items.name)
        item.append (items.quantity)
        item.append (items.price)
        item.append (items.unit)
        data.append (item)
    print (data)

# Function for get price value from database
def get_price ():
    Session = sessionmaker (bind=engine)
    session = Session()
    query = session.query (Bid_Items).all()
    data = []
    for item in query:
        values = []
        value = item.quantity * item.price
        values.append (value)
        data.append (sum (values))
    return data 

# Function to delete items from bid database
def delete_db ():
    Session = sessionmaker (bind=engine)
    session = Session()
    session.query (Bid_Items).delete('evaluate')
    session.commit()
    