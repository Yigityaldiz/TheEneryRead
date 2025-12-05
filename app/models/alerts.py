from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class AnomalyAlert(Base):
    __tablename__ = "anomaly_alerts"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    type = Column(String, nullable=False)  # e.g., "VOLTAGE_IMBALANCE"
    severity = Column(String, nullable=False)  # "WARNING", "CRITICAL"
    description = Column(Text, nullable=True)
    is_resolved = Column(Boolean, default=False)
