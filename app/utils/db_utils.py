import os
from sqlalchemy import create_engine

db_url = os.getenv("DB_URL")
engine = create_engine(db_url)
