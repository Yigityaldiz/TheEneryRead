from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.readings import get_readings_history
from app.crud.machines import get_machine

router = APIRouter(prefix="/api/machines", tags=["Machines"])

@router.get("/{machine_id}/history")
async def get_machine_history(machine_id: int, db: AsyncSession = Depends(get_db)):
    machine = await get_machine(db, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
        
    readings = await get_readings_history(db, machine_id, hours=1)
    
    return {
        "machine": machine.name,
        "history": readings
    }
