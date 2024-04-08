from models.company_db import Company_Items, engine
from sqlalchemy.orm import sessionmaker
from models.company_db import Company_Items

# Function to read info about company from database
def read_company_db () -> list:
    Session = sessionmaker (bind=engine)
    session = Session()
    query = session.query (Company_Items).all()
    names = []
    for user in query:
        item = []
        item.append (user.name)
        item.append (user.address)
        item.append (user.oib)
        names.append (item)
    return names