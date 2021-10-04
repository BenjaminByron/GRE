import psycopg2
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from word import Word
from flask_sqlalchemy import SQLAlchemy
import dash

engine = create_engine('postgresql://iyoalfhnzaqaqy:54e38dd1ecf2b4a25c9158b51c3ed0efbc8a8336c5c721f9ba5d7af65b7b6315@ec2-54-170-163-224.eu-west-1.compute.amazonaws.com:5432/d7ssmu85htau94')

Session=sessionmaker(bind=engine)
session=Session()

def get_words():
    s = ''
    words = session.query(Word).all()
    for w in words:
        # print(w.__dict__)
        s = s + w.word + ', '
    get_baskets()
    return s

def get_topics():
    ''' Get the list of topics in the database by extracting the unique values from the topics column. '''
    topics = []
    for topic in session.query(Word.topic).distinct():
        topics.append(topic[0])
    return topics

def get_word_by_topic(topics):
    ''' Generate list of dictionaries by topic. '''
    baskets = []
    for topic_query in topics:
        basket = {}
        basket['topic'] = topic_query
        basket['words'] = []
        for w in session.query(Word).filter_by(topic=topic_query).all():
            basket['words'].append(w.word)
        baskets.append(basket)
    return baskets

def get_baskets():
    ''' Execute basket creation. '''
    topics = get_topics()
    baskets = get_word_by_topic(topics)
    print(baskets)