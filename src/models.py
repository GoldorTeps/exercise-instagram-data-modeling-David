import os
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from eralchemy import render_er

Base = declarative_base()

# Enum para el campo 'type' en la tabla 'Media'
class MediaType(Enum):
    image = 'image'
    video = 'video'

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    # Relación con la tabla Follower
    followers = relationship('Follower', foreign_keys='Follower.user_to_id')
    following = relationship('Follower', foreign_keys='Follower.user_from_id')
    
    # Relación con la tabla Comment
    comments = relationship('Comment', back_populates='author')
    
    # Relación con la tabla Post
    posts = relationship('Post', back_populates='user')

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    
    # Relación con la tabla User
    author = relationship('User', back_populates='comments')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Relación con la tabla User
    user = relationship('User', back_populates='posts')

    # Relación con la tabla Media
    media = relationship('Media', back_populates='post')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)  
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    
    # Relación con la tabla Post
    post = relationship('Post', back_populates='media')



# Crea la base de datos y las tablas
engine = create_engine('sqlite:///mydatabase.db')
Base.metadata.create_all(engine)

# Para generar un diagrama de entidad-relación (ER) utilizando eralchemy
try:
    render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e


