from database import Base, engine
from models import Log

print("Creating a Database....")

Base.metadata.create_all(engine)
