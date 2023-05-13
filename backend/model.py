from sqlalchemy import Column, String, ForeignKey, create_engine, Integer, String, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import relationship

engine = create_engine("mariadb+mariadbconnector://root:12345678@127.0.0.1:3307/restapidb")

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    captions = relationship('Caption', back_populates='user')
    favourites = relationship('Favourite', back_populates='user')
    images = relationship('Image', back_populates='user')

class Caption(Base):
    __tablename__ = 'caption'

    id = Column(Integer, primary_key=True)
    caption_text = Column(String(255), nullable=False)
    image_id = Column(Integer, ForeignKey('image.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    release_at = Column(DateTime)

    tags = relationship('Tag', secondary='caption_tag', back_populates='captions')
    user = relationship('User', back_populates='captions')
    favourites = relationship('Favourite', back_populates='caption')

class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    tag_text = Column(String(255), nullable=False, unique=True)

    captions = relationship('Caption', secondary='caption_tag', back_populates='tags')

caption_tag = Table('caption_tag', Base.metadata,
                    Column('caption_id', Integer, ForeignKey('caption.id')),
                    Column('tag_id', Integer, ForeignKey('tag.id')))

class Favourite(Base):
    __tablename__ = 'favourite'

    id = Column(Integer, primary_key=True)
    caption_id = Column(Integer, ForeignKey('caption.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='favourites')
    caption = relationship('Caption', back_populates='favourites')

class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    image_url = Column(String(255), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='images')
    captions = relationship('Caption', back_populates='image')

Base.metadata.create_all(engine)