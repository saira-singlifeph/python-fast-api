from database import Base
from sqlalchemy import String, Integer, Column, DateTime, Text
from datetime import datetime
from sqlalchemy.sql import func


class Log(Base):
    __tablename__   ='logs'
    id              = Column(Integer,primary_key=True,autoincrement=True)
    message         = Column(Text,nullable=False)
    priority        = Column(String(255),nullable=False)
    source          = Column(String(255),nullable=False)
    created_at      = Column(DateTime(255),default=datetime.utcnow)
    updated_at      = Column(DateTime(255), default=datetime.now, onupdate=func.now())
    

    
    