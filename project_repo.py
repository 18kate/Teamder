from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config.config import settings
from src.data.entity.models import Base


def create_db():
    engine = create_engine(settings.db_url)
    Base.metadata.create_all(engine)


def connect_db():
    engine = create_engine(settings.db_url)
    session = Session(bind=engine.connect())
    return session
