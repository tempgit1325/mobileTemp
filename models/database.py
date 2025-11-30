from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

db = os.getenv("DATABASE")
postgres_passw = os.getenv("POSTGRES_PASSWORD")
postgres_user = os.getenv("POSTGRES_USER")

DATABASE_URL = f"postgresql+psycopg2://{postgres_user}:{postgres_passw}@localhost:5432/{db}"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

Base = declarative_base()
