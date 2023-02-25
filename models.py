from database import Base
from sqlalchemy import String, Integer, Column, DateTime, Text, Enum
from datetime import datetime
from sqlalchemy.sql import func
import enum

class prioritiesEnum(enum.Enum):
    urgent  = "urgent"
    high    = "high"
    medium  = "medium"
    low     = "low"

class Log(Base):
    __tablename__   ='logs'
    id              = Column(Integer,primary_key=True,autoincrement=True)
    log_name        = Column(String(255), nullable=False)
    message         = Column(Text,nullable=False)
    priority        = Column(Enum(prioritiesEnum),nullable=False)
    source          = Column(String(255),nullable=False)
    created_at      = Column(DateTime(255),default=datetime.utcnow)
    updated_at      = Column(DateTime(255), default=datetime.now, onupdate=func.now())
    

    
    