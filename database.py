from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# connect to the dabase
engine=create_engine("postgresql://postgres:1234@localhost/Log", echo=True)

Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)