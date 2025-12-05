import asyncio
from app.services.abysis_api import abysis_client
import json

async def main():
    try:
        print("Logging in...")
        await abysis_client.login()
        print(f"SessionId: {abysis_client.token}")
        
        print("\n--- FETCHING MATRIX DATA ---")
        data = await abysis_client.get_index_values_matrix()
      
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("---------------------")
    except Exception as e:
        print(f"\n--- FAILED ---")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
