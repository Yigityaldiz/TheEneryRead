from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.core.database import Base

class ElectricReading(Base):
    __tablename__ = "electric_readings"

    time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"), primary_key=True, nullable=False)
    
    active_energy = Column(Float)
    
    voltage_l1 = Column(Float)
    voltage_l2 = Column(Float)
    voltage_l3 = Column(Float)
    
    current_l1 = Column(Float)
    current_l2 = Column(Float)
    current_l3 = Column(Float)

    # Note: create_hypertable logic will be handled in initialization
