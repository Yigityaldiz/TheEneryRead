from sqlalchemy import text
from app.core.database import engine, Base
# Import models to ensure they are registered with Base
from app.models import Machine, ElectricReading, AnomalyAlert

async def init_db():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
        
        # Convert electric_readings to hypertable
        try:
            # We use execute directly on the connection
            await conn.execute(text("SELECT create_hypertable('electric_readings', 'time', if_not_exists => TRUE);"))
            print("Hypertable 'electric_readings' created or already exists.")
        except Exception as e:
            print(f"Hypertable creation warning (might be expected): {e}")
