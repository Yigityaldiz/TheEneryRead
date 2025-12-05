from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Machine

async def get_machine(db: AsyncSession, machine_id: int):
    result = await db.execute(select(Machine).filter(Machine.id == machine_id))
    return result.scalars().first()

async def get_machine_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(Machine).filter(Machine.name == name))
    return result.scalars().first()

async def get_machines(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Machine).offset(skip).limit(limit))
    return result.scalars().all()

async def create_machine(db: AsyncSession, machine: Machine):
    db.add(machine)
    await db.commit()
    await db.refresh(machine)
    return machine
