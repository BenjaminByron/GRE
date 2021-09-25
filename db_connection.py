import psycopg2
import pandas
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from word import Word


engine = create_engine('postgresql://alejandra.gutierrez:aleseb99@localhost/GRE')

Session=sessionmaker(bind=engine)
session=Session()

def get_words():
    s = ''
    words = session.query(Word).all()
    for w in words:
        s = s + w.word + ', '
    return s