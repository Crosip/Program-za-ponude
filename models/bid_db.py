from sqlalchemy import Column, Float, MetaData, String, Table, create_engine
from sqlalchemy.orm import declarative_base

# Create and declare database for bid info
db_url = 'sqlite:///Bid_Database.db'

engine = create_engine (db_url)

Base = declarative_base()

class Bid_Items (Base):
    __tablename__ = 'data'
    
    name = Column (String, primary_key = True)
    quantity = Column (Float)
    price = Column (Float)
    unit = Column (String)


Base.metadata.create_all (engine)