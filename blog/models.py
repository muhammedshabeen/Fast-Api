from sqlalchemy import Column,Integer,String,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String)
    body = Column(String)
    creator = relationship("User",back_populates="blogs")
    user_id = Column(Integer, ForeignKey("users.id"))



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)  # Add unique constraint for uniqueness
    email = Column(String(255), unique=True)  # Add unique constraint for uniqueness
    password = Column(String(255))
    blogs = relationship("Blog",back_populates='creator')