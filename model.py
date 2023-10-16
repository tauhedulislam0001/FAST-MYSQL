from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    
    posts = relationship("Post", back_populates = "author")
    
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    author = relationship("User", back_populates="posts")