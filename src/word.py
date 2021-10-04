import psycopg2
import pandas
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Word(Base):
    __tablename__ = 'word'
    word = Column('Word', String(32), primary_key=True)
    topic = Column('Topic', String(32))
