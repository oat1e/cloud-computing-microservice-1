"""
SQLAlchemy database models for User and MatchaSession.
"""
from sqlalchemy import Column, String, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
import uuid

from utils.database import Base


class UserDB(Base):
    """SQLAlchemy model for User table."""
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    username = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=True)
    favorite_matcha_powder = Column(String(255), nullable=True)
    favorite_matcha_place = Column(String(255), nullable=True)
    matcha_budget = Column(Float, nullable=True)
    join_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to matcha sessions
    matcha_sessions = relationship("MatchaSessionDB", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserDB(id={self.id}, username={self.username})>"


class MatchaSessionDB(Base):
    """SQLAlchemy model for MatchaSession table."""
    __tablename__ = "matcha_sessions"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=True, index=True)
    session_date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    matcha_type = Column(String(50), nullable=False)
    brand = Column(String(255), nullable=True)
    rating = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to user
    user = relationship("UserDB", back_populates="matcha_sessions")

    def __repr__(self):
        return f"<MatchaSessionDB(id={self.id}, session_date={self.session_date})>"

