from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.orm import declarative_base

# Create and declare database for company
db_url = 'sqlite:///Company_Database.db'

engine = create_engine (db_url)

Base = declarative_base()

class Company_Items (Base):
    __tablename__ = 'data'
    
    name = Column (String)
    oib = Column (Integer, primary_key = True)
    address = Column (String)


    


Base.metadata.create_all (engine)

# Create class to hold data about company
class Company_Data ():
    def __init__(self, name, oib, address):
        
        self.name = name
        self.oib = oib
        self.address = address

    def data_to_dict (self) -> dict:
        data = {
            'Name' : self.name,
            'Address' : self.address,
            'OIB' : self.oib
        }
        return data