from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base   

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True)

    user_sender = Column(Integer, ForeignKey("users.id"))
    user_receiver = Column(Integer, ForeignKey("users.id"), nullable=True)

    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    delivery_lat = Column(Float)
    delivery_lng = Column(Float)

    message_target = Column(String, default="package is fragile")

    status = Column(String, default="waiting")
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="shipments_sent", foreign_keys=[user_sender])
    receiver = relationship("User", back_populates="shipments_received", foreign_keys=[user_receiver])


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    shipments_sent = relationship("Shipment", back_populates="sender", foreign_keys="[Shipment.user_sender]")
    shipments_received = relationship("Shipment", back_populates="receiver", foreign_keys="[Shipment.user_receiver]")
