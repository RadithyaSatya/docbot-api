import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from app.db import Base


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    document_id = Column(Integer, ForeignKey("documents.id"))

    document = relationship("Document", back_populates="history", cascade="all")
