from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import get_settings

settings = get_settings()

engine = create_engine(settings.db_connect_str, echo=True)
db_session = Session(engine)
