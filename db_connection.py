import dash
import psycopg2
from word import Word
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer

engine = create_engine('postgresql://iyoalfhnzaqaqy:54e38dd1ecf2b4a25c9158b51c3ed0efbc8a8336c5c721f9ba5d7af65b7b6315@ec2-54-170-163-224.eu-west-1.compute.amazonaws.com:5432/d7ssmu85htau94')

Session=sessionmaker(bind=engine)
session=Session()


def get_topics():
    ''' Get the list of topics in the database by extracting the unique values from the topics column. '''
    topics = []
    for topic in session.query(Word.topic).distinct():
        topics.append(topic[0])
    return topics

def get_words_by_topic(topic_query):
    ''' Get list of words for a specific topic. '''
    words = []
    for w in session.query(Word).filter_by(topic=topic_query).all():
        words.append(w.word)
    return words
