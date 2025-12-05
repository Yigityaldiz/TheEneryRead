from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ElectricReading, AnomalyAlert

async def get_latest_reading(db: AsyncSession, machine_id: int):
    result = await db.execute(
        select(ElectricReading)
        .filter(ElectricReading.machine_id == machine_id)
        .order_by(desc(ElectricReading.time))
        .limit(1)
    )
    return result.scalars().first()

async def get_readings_history(db: AsyncSession, machine_id: int, hours: int = 1):
    since = datetime.utcnow() - timedelta(hours=hours)
    result = await db.execute(
        select(ElectricReading)
        .filter(ElectricReading.machine_id == machine_id, ElectricReading.time >= since)
        .order_by(ElectricReading.time)
    )
    return result.scalars().all()

async def get_recent_alerts(db: AsyncSession, hours: int = 24):
    since = datetime.utcnow() - timedelta(hours=hours)
    result = await db.execute(
        select(AnomalyAlert)
        .filter(AnomalyAlert.detected_at >= since)
        .order_by(desc(AnomalyAlert.detected_at))
    )
    return result.scalars().all()

async def get_alerts_count(db: AsyncSession):
    # For dashboard summary
    # Note: count() is tricky in async sqlalchemy sometimes, using len() of list for MVP or func.count
    from sqlalchemy import func
    result = await db.execute(select(func.count(AnomalyAlert.id)))
    return result.scalar()

async def create_reading(db: AsyncSession, reading: ElectricReading):
    db.add(reading)
    await db.commit()
    await db.refresh(reading)
    return reading

async def create_alert(db: AsyncSession, alert: AnomalyAlert):
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert
