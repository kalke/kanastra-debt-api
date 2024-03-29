import os
from dotenv import load_dotenv

from sqlalchemy.orm import declarative_base

load_dotenv()

class Config(object):
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'mysql+pymysql://root:root@localhost:3306/kanastra')
    Base = declarative_base()


config = Config()
