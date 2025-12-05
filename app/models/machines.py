from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    remote_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    specs = Column(JSON, nullable=True)  # Nominal voltage/current limits
    created_at = Column(DateTime(timezone=True), server_default=func.now())
