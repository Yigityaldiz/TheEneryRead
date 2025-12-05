import json
from app.core.database import AsyncSessionLocal
from app.crud.machines import get_machine_by_name
from app.crud.readings import get_latest_reading, get_recent_alerts

async def get_machine_status(machine_name: str):
    """
    Get the latest status (voltage, current, energy) of a specific machine by name.
    """
    async with AsyncSessionLocal() as db:
        machine = await get_machine_by_name(db, machine_name)
        if not machine:
            return json.dumps({"error": "Machine not found"})
        
        reading = await get_latest_reading(db, machine.id)
        if not reading:
            return json.dumps({"status": "No data available", "machine": machine.name})
        
        return json.dumps({
            "machine": machine.name,
            "timestamp": str(reading.time),
            "voltage": {
                "L1": reading.voltage_l1,
                "L2": reading.voltage_l2,
                "L3": reading.voltage_l3
            },
            "current": {
                "L1": reading.current_l1,
                "L2": reading.current_l2,
                "L3": reading.current_l3
            },
            "active_energy": reading.active_energy
        })

async def get_alerts_tool():
    """
    Get the list of anomaly alerts detected in the last 24 hours.
    """
    async with AsyncSessionLocal() as db:
        alerts = await get_recent_alerts(db, hours=24)
        if not alerts:
            return json.dumps({"alerts": [], "message": "No alerts in the last 24 hours."})
        
        result = []
        for alert in alerts:
            result.append({
                "id": alert.id,
                "machine_id": alert.machine_id,
                "type": alert.type,
                "severity": alert.severity,
                "description": alert.description,
                "time": str(alert.detected_at)
            })
        return json.dumps({"alerts": result})

# Tool Definitions for OpenAI
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_machine_status",
            "description": "Get the latest voltage, current, and energy readings for a specific machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "machine_name": {
                        "type": "string",
                        "description": "The name of the machine, e.g., 'CNC Pres 1' or 'Mock Machine 1'"
                    }
                },
                "required": ["machine_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_alerts_tool",
            "description": "Get recent anomaly alerts from the system.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]
