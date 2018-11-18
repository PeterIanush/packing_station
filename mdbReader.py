from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import easygui

Base = declarative_base()

class Reader(Base):

    def __init__(self):
        pass

    def session(self):

        engine = create_engine(r'access:///C:/Users/peter.ianush/Desktop/main/Spares/aeu_spares_be.mdb')
        self.session = sessionmaker(bind=engine)


    def readerMDB(self):

        pass

