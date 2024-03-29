from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config

SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
config.Base.metadata.create_all(bind=engine)

@contextmanager
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
