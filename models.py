from database import Base
from sqlalchemy import String, Integer, Column, DateTime, Text, Enum
from datetime import datetime
from sqlalchemy.sql import func
import enum


class priorities_enum(enum.Enum):
    urgent = "urgent"
    high = "high"
    medium = "medium"
    low = "low"


class source_enum(enum.Enum):
    unknown = "unknown"
    customer = "customer"
    internal = "internal"
    other = "other"


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    log_name = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(Enum(priorities_enum), nullable=False)
    source = Column(Enum(source_enum), nullable=False)
    created_at = Column(DateTime(255), default=datetime.utcnow)
    updated_at = Column(DateTime(255), default=datetime.now,
                        onupdate=func.now())
