from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.readings import get_alerts_count, get_latest_reading
from app.crud.machines import get_machines

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    # 1. Active Alerts Count
    alerts_count = await get_alerts_count(db)
    
    # 2. Total Consumption (Sum of latest active_energy from all machines)
    machines = await get_machines(db)
    total_energy = 0.0
    
    for machine in machines:
        reading = await get_latest_reading(db, machine.id)
        if reading:
            total_energy += reading.active_energy
            
    return {
        "active_alerts": alerts_count,
        "total_energy_consumption": total_energy,
        "active_machines": len(machines)
    }
