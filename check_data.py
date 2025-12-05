import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.readings import ElectricReading

async def main():
    async with AsyncSessionLocal() as session:
        print("Fetching REAL data from 2025-12-04...")
        from datetime import datetime
        target_date = datetime(2025, 12, 4)
        result = await session.execute(
            select(ElectricReading)
            .where(ElectricReading.time >= target_date)
            .where(ElectricReading.time < datetime(2025, 12, 5))
            .order_by(ElectricReading.time.desc())
            .limit(10)
        )
        readings = result.scalars().all()
        
        if not readings:
            print("No readings found.")
        else:
            print(f"{'Time':<30} | {'Active Energy':<15} | {'Voltage L1':<10}")
            print("-" * 60)
            for r in readings:
                print(f"{str(r.time):<30} | {r.active_energy:<15} | {r.voltage_l1:<10}")

if __name__ == "__main__":
    asyncio.run(main())
