from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import SessionLocal
from datetime import datetime
from sqlalchemy import and_, cast, String
from sqlalchemy.sql import func, desc
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


class Log(BaseModel):  # serializer
    log_name: str
    message: str
    priority: models.priorities_enum
    source: models.source_enum

    class Config:
        orm_mode = True


class Logs(BaseModel):
    log_name: str
    message: str
    priority: models.priorities_enum
    source: models.source_enum
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Statistic(BaseModel):
    urgent: int
    high: int
    medium: int
    low: int


db = SessionLocal()

levels = ('urgent', 'high', 'medium', 'low')


@app.get("/logs/query",
         response_model=List[Logs],
         status_code=status.HTTP_200_OK
         )
async def query_logs(
    level: str = None,
    from_date: str = None,
    to_date: str = None,
    source: str = None,
    query_all: bool = False,
    log_name: str = None
):
    Logs = models.Log

    if level is not None:
        if query_all is False:
            if from_date and to_date is not None:
                query = db.query(Logs).filter(
                    and_(cast(Logs.priority, String).like(level),
                         (func.date(Logs.created_at).between(from_date, to_date)))).all()
                return query

            if source is not None:
                query = db.query(Logs).filter(
                    and_(cast(Logs.priority, String).like(level), (cast(Logs.source, String).like(source)))).all()
                return query

            query = db.query(Logs).filter(
                (cast(Logs.priority, String).like(level))).all()
            return query

        if query_all is True:
            query = db.query(Logs).filter(and_(cast(Logs.priority, String).like(level)),
                                          (cast(Logs.source, String).like(source)), (func.date(Logs.created_at).between(from_date, to_date))).all()
            return query

        query = db.query(Logs).filter(
            (cast(Logs.priority, String).like(level))).all()
        return query

    if log_name is not None:

        search = "%{}%".format(log_name)
        query = db.query(Logs).filter((Logs.log_name.like(search))).all()
        return query

    return []


@app.get("/logs",
         response_model=List[Logs],
         status_code=status.HTTP_200_OK
         )
def get_all_logs():
    logs = db.query(models.Log).order_by(desc(models.Log.updated_at)).all()
    return logs


@app.get("/logs/statistic/count",
         status_code=status.HTTP_200_OK
         )
def statistic_count():
    Logs = models.Log
    count = []
    for level in levels:
        query = db.query(Logs).filter(
            (cast(Logs.priority, String).like(level))).count()
        count.append({"count": query, "level": level})

    return count


@app.get("/logs/statistic/data",
         status_code=status.HTTP_200_OK,
         )
def statistic_data(
    priority_level: str = None,
    source_type: str = None,
):

    Logs = models.Log
    sources = ("unknown", "customer", "internal", "other")
    list_items = []

    if source_type is not None:
        for level in levels:
            query = db.query(Logs).filter(
                and_(cast(Logs.priority, String).like(level), (cast(Logs.source, String).like(source_type)))).count()
            list_items.append({"type": level, "logs": query})

        return list_items

    if priority_level is not None:
        for source in sources:
            query = db.query(Logs).filter(
                and_(cast(Logs.priority, String).like(priority_level), (cast(Logs.source, String).like(source)))).count()
            list_items.append({"type": source, "logs": query})

        return list_items

    return []


@app.get("/logs/{log_id}",
         response_model=Logs,
         status_code=status.HTTP_200_OK
         )
def get_log(log_id: int):
    log = db.query(models.Log).get({"id": log_id})
    return log


@app.post("/logs",
          response_model=Log,
          status_code=status.HTTP_201_CREATED
          )
def create_log(log: Log):
    new_log = models.Log(
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
async def update_log(log_id: int, details: Log):
    log_to_update = db.query(models.Log).get({"id": log_id})

    if log_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Log Not Found")

    log_to_update.message = details.message
    log_to_update.priority = details.priority
    log_to_update.source = details.source
    log_to_update.log_name = details.log_name

    db.commit()
    return {"success": "true"}


@app.delete("/logs/{log_id}",
            response_model=Logs,
            status_code=status.HTTP_200_OK
            )
def delete_log(log_id: int):
    log_to_delete = db.query(models.Log).get({"id": log_id})

    if log_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Log Not Found")

    db.delete(log_to_delete)
    db.commit()
    return log_to_delete
