import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(50), nullable = False)
    email = Column(String(100), nullable = False, unique = True)
    password_hash = Column(Text, nullable = False)
    created_at = Column(DateTime, default = datetime.datetime.utcnow)

    documents = relationship("Document", back_populates="user", cascade="all")