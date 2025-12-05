import asyncio
from celery import shared_task
from app.core.database import AsyncSessionLocal
from app.services.abysis_api import abysis_client
from app.crud.machines import get_machine_by_name, create_machine
from app.crud.readings import create_reading, create_alert
from app.models.machines import Machine
from app.models.readings import ElectricReading
from app.models.alerts import AnomalyAlert
from datetime import datetime

@shared_task
def fetch_and_process_data():
    async def _process():
        async with AsyncSessionLocal() as session:
            print("Fetching data from Abysis API (Instant)...")
            try:
                # 1. Fetch data from API
                response = await abysis_client.get_instant_values()
                records = response.get("Value", [])
                
                if not records:
                    print("No data received from Abysis API.")
                    return

                # 2. Group by timestamp and meter
                # Structure: { (timestamp, meter_id): { 'voltage_l1': ..., ... } }
                grouped_data = {}
                
                # Mapping from Abysis Code to DB fields
                CODE_MAP = {
                    '31.7.0': 'current_l1',
                    '51.7.0': 'current_l2',
                    '71.7.0': 'current_l3',
                    '32.7.0': 'voltage_l1',
                    '52.7.0': 'voltage_l2',
                    '72.7.0': 'voltage_l3',
                    '1.8.0': 'active_energy'
                }

                for record in records:
                    meter_id = record.get("MeterId")
                    timestamp_str = record.get("dateTime") 
                    if not timestamp_str:
                        continue
                        
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str)
                    except ValueError:
                        continue
                    
                    key = (timestamp, meter_id)
                    if key not in grouped_data:
                        grouped_data[key] = {}
                    
                    index_code = record.get("IndexInfo", {}).get("Code")
                    if index_code in CODE_MAP:
                        val = record.get("FixedValue", 0.0)
                        grouped_data[key][CODE_MAP[index_code]] = val

                # 3. Save to DB
                for (timestamp, meter_id), values in grouped_data.items():
                    # Ensure machine exists
                    machine_name = f"Meter-{meter_id}"
                    machine = await get_machine_by_name(session, machine_name)
                    if not machine:
                        machine = await create_machine(session, Machine(
                            name=machine_name,
                            remote_id=str(meter_id),
                            specs={"source": "Abysis API"}
                        ))
                    
                    # Create reading
                    reading = ElectricReading(
                        time=timestamp,
                        machine_id=machine.id,
                        active_energy=values.get('active_energy', 0.0),
                        voltage_l1=values.get('voltage_l1', 0.0),
                        voltage_l2=values.get('voltage_l2', 0.0),
                        voltage_l3=values.get('voltage_l3', 0.0),
                        current_l1=values.get('current_l1', 0.0),
                        current_l2=values.get('current_l2', 0.0),
                        current_l3=values.get('current_l3', 0.0)
                    )
                    await create_reading(session, reading)
                    print(f"Saved reading for {machine_name} at {timestamp}")

                    # 4. Anomaly Detection
                    v1, v2, v3 = reading.voltage_l1, reading.voltage_l2, reading.voltage_l3
                    if abs(v1 - v2) > 15 or abs(v2 - v3) > 15 or abs(v1 - v3) > 15:
                        alert = AnomalyAlert(
                            machine_id=machine.id,
                            detected_at=timestamp,
                            type="Voltage Imbalance",
                            severity="High",
                            description=f"Voltage imbalance detected: L1={v1}, L2={v2}, L3={v3}",
                            is_resolved=False
                        )
                        await create_alert(session, alert)
                        print(f"Anomaly detected for {machine_name}")

            except Exception as e:
                print(f"Error in fetch_and_process_data: {e}")

    # Run async logic in sync Celery task
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_process())
    loop.close()
    return "Data processed successfully"
