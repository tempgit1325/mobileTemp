from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime,Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import ENUM
from dotenv import load_dotenv
import os

load_dotenv() 

db = os.getenv("DATABASE")
postgres_passw = os.getenv("POSTGRES_PASSWORD")
postgres_user = os.getenv("POSTGRES_USER")

DATABASE_URL = f"postgresql+psycopg2://{postgres_user}:{postgres_passw}@localhost:5432/{db}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True)

    user_sender = Column(Integer, ForeignKey("users.id"))
    user_receiver = Column(Integer, ForeignKey("users.id"), nullable=True)

    pickup_lat = Column(Float)
    pickup_lng = Column(Float)

    delivery_lat = Column(Float)
    delivery_lng = Column(Float)

    status = Column(String, default="waiting")
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="shipments_sent", foreign_keys=[user_sender])
    receiver = relationship("User", back_populates="shipments_received", foreign_keys=[user_receiver])
                                                                                       
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    shipments_sent = relationship(
        "Shipment",
        back_populates="sender",
        foreign_keys=[Shipment.user_sender]
    )

    shipments_received = relationship(
        "Shipment",
        back_populates="receiver",
        foreign_keys=[Shipment.user_receiver]
    )
