from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_db_connection():
    engine = create_engine('mysql+mysqlconnector://root:chu=athuf8wrE=IhEde1@localhost/grindworld')
    Session = sessionmaker(bind=engine)
    return Session()
