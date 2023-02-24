from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import SessionLocal
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.sql import func
import models

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# models
class Log(BaseModel): #serializer
    log_name: str
    message: str
    priority: str
    source: str
    
    class Config:
        orm_mode=True
        
        
class Logs(BaseModel):
    log_name: str
    message: str
    priority: str
    source: str
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode=True

db = SessionLocal()

@app.get("/logs/query",
    response_model=List[Logs], 
    status_code=status.HTTP_200_OK     
    )
async def query_logs(level: str = "", createdDate: str = ""):
    Logs = models.Log
    query = db.query(Logs).filter(
        and_(Logs.priority.like(level),
        (func.date(Logs.created_at) == createdDate))
    ).all()
    
    return query
    

@app.get("/logs", 
        response_model=List[Logs], 
        status_code=status.HTTP_200_OK
        )
def get_all_logs():
    logs = db.query(models.Log).all()
    return logs
    

@app.get("/logs/{log_id}", 
        response_model=Log, 
        status_code=status.HTTP_200_OK
        )
def get_log(log_id:int):
    log = db.query(models.Log).get({"id": log_id})
    return log


@app.post("/logs", 
    response_model=Log, 
    status_code=status.HTTP_201_CREATED
    )
def create_log(log:Log):
    new_log=models.Log(
        log_name=log.log_name,
        message=log.message,
        priority=log.priority,
        source=log.source
    )
    
    db.add(new_log)
    db.commit()
    
    return new_log


@app.put("/logs/{log_id}",
    status_code=status.HTTP_200_OK
    )
async def update_log(log_id:int, log:Log):
    log_to_update = db.query(models.Log).get({"id": log_id})
    
    if log_to_update is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Log Not Found")
    log_to_update.message = log.message
    log_to_update.priority = log.priority
    log_to_update.source = log.source
    log_to_update.log_name = log.log_name

    db.commit()
    return { "success": "true" }
    

@app.delete("/logs/{log_id}",
    response_model=Logs,
    status_code=status.HTTP_200_OK
    )
def delete_log(log_id:int):
    log_to_delete = db.query(models.Log).get({"id": log_id})
    
    if log_to_delete is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Log Not Found")
    
    db.delete(log_to_delete)
    db.commit()
    return log_to_delete
    
    




