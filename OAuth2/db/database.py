from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, DeclarativeBase
from config import get_settings

settings = get_settings()

engine = create_engine(settings.db_connect_str, echo=True)
session = Session(engine)

class Base(DeclarativeBase):
    pass

