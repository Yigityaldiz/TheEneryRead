import asyncio
from app.services.abysis_api import abysis_client

async def test_login():
    print("Testing Abysis Login...")
    try:
        data = await abysis_client.login()
        print("\n--- LOGIN SUCCESS ---")
        print(f"SessionId: {abysis_client.token}")
        
        print("\n--- FETCHING DATA ---")
        readings = await abysis_client.get_instant_values()
        print(readings)
        print("---------------------")
    except Exception as e:
        print(f"\n--- LOGIN FAILED ---")
        print(e)

if __name__ == "__main__":
    asyncio.run(test_login())
