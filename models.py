from sqlalchemy import Column, Integer, String, DateTime, Text, LargeBinary,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,nullable=False)
    password = Column(String,unique=True,nullable=False)
    episodes = relationship("Episode", back_populates="user", cascade="all, delete")

class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    title = Column(String)
    story = Column(Text)
    image_data = Column(LargeBinary) 
    user_id = Column(Integer,ForeignKey("users.id")) 
    user = relationship("User", back_populates="episodes")
    

    
