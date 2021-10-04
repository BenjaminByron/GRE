import psycopg2
import pandas
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from word import Word
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash

engine = create_engine('postgresql://iyoalfhnzaqaqy:54e38dd1ecf2b4a25c9158b51c3ed0efbc8a8336c5c721f9ba5d7af65b7b6315@ec2-54-170-163-224.eu-west-1.compute.amazonaws.com:5432/d7ssmu85htau94')

Session=sessionmaker(bind=engine)
session=Session()

def get_words():
    s = ''
    words = session.query(Word).all()
    for w in words:
        s = s + w.word + ', '
    return s