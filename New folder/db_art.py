import sys

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Unicode#, LONGBLOB

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

# from sqlalchemy_imageattach.entity import Image, image_attachment

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

class UserPicture(Base):
	__tablename__='userimg'

	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	user = relationship('User')

class Fotos(Base):
    __tablename__ = 'fotos'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    tag = Column(String(250), nullable=False)
    # data= Column(LONGBLOB)
    folder =  Column(String(250), nullable=False)
    creacion = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))

class Comentarios(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    creacion = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    fotos_id = Column(Integer, ForeignKey('fotos.id'))   
		
class LikesDislikes(Base):
    __tablename__ = 'likes_dislikes'

    id = Column(Integer, primary_key=True)
    foto_id = Column(Integer, ForeignKey('fotos.id'))
    like = Column(Integer,nullable=False)
    dislike = Column(Integer,nullable=False)
    creacion = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
     

engine = create_engine('sqlite:///db_art.db')


Base.metadata.create_all(engine)