import httpx
from app.core.config import settings

class AbysisClient:
    def __init__(self):
        self.base_url = settings.ABYSIS_API_URL
        self.username = settings.ABYSIS_USERNAME
        self.password = settings.ABYSIS_PASSWORD
        self.department_code = settings.ABYSIS_DEPARTMENT_CODE
        self.token = None
        self.authorized_meters = []

    async def login(self):
        """
        Authenticate with Abysis API.
        Endpoint: GET /api/Authentication/Login
        Format: department_code={code}@{api_key}
        """
        if not self.department_code:
            self.department_code = "0"
            
        # Construct department_code as required: CODE@API_KEY
        dept_param = f"{self.department_code}@{settings.ABYSIS_API_KEY}"
        
        params = {
            "username": self.username,
            "password": self.password,
            "department_code": dept_param
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/Authentication/Login", 
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get("Result", {}).get("ResultType") == "Successfull":
                    self.token = data.get("Value")  # SessionId
                    self.authorized_meters = data.get("AuthorizedMeters", [])
                    print(f"Login Successful. SessionId: {self.token}")
                    return data
                else:
                    raise Exception(f"Login failed: {data.get('Result', {}).get('Info')}")
                    
            except Exception as e:
                print(f"An error occurred during login: {e}")
                raise

    async def get_instant_values(self):
        """
        Fetch instant values for authorized meters.
        Endpoint: GET /api/Indexes/IndexValueList
        """
        if not self.token or not self.authorized_meters:
            await self.login()
            
        if not self.authorized_meters:
            print("No authorized meters found.")
            return []

        if not self.authorized_meters:
            print("No authorized meters found.")
            return []

        # Use the first meter
        meter = self.authorized_meters[0]
        
        department_id = meter.get("DepartmentId")
        subscriber_id = meter.get("SubscriberId")
        main_meter_id = meter.get("Id")
        
        if not main_meter_id:
             print("No valid MeterId found.")
             return []

        print(f"Using Meter - Dept: {department_id}, Sub: {subscriber_id}, Meter: {main_meter_id}")
        
        # Date range: Last 48 hours to catch test data
        import datetime
        end_date = datetime.datetime.utcnow()
        begin_date = end_date - datetime.timedelta(hours=48)
        
        # Format dates as ISO 8601
        fmt = "%Y-%m-%dT%H:%M:%SZ"
        
        params = {
            "SessionId": self.token,
            "departmentId": department_id,
            "subscriberId": subscriber_id,
            "MeterId": main_meter_id,
            "IndexId": 0, 
            "BeginDate": begin_date.strftime(fmt),
            "EndDate": end_date.strftime(fmt),
            "api_key": settings.ABYSIS_API_KEY
        }
        
        # Try omitting IndexId first, or guess 0
        # params["IndexId"] = 0 

        headers = {}
        if settings.ABYSIS_API_KEY:
            headers["api_key"] = settings.ABYSIS_API_KEY

        async with httpx.AsyncClient() as client:
            try:
                # Note: Swagger showed api_key in query params too.
                response = await client.get(
                    f"{self.base_url}/api/Indexes/IndexValueList", 
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error fetching data: {e}")
                # If 404, maybe print the url
                if hasattr(e, 'request'):
                     print(f"Request URL: {e.request.url}")
                raise

    async def get_index_values_matrix(self):
        """
        Fetch matrix values for authorized meters.
        Endpoint: GET /api/Indexes/IndexValuesMatrix
        """
        if not self.token or not self.authorized_meters:
            await self.login()
            
        if not self.authorized_meters:
            print("No authorized meters found.")
            return []

        # Use the first meter
        meter = self.authorized_meters[0]
        main_meter_id = meter.get("Id")
        department_id = meter.get("DepartmentId")
        
        if not main_meter_id:
             print("No valid MeterId found.")
             return []

        print(f"Fetching Matrix for Meter: {main_meter_id}, Dept: {department_id}")
        
        # Date range: Last 1 hour
        import datetime
        end_date = datetime.datetime.utcnow()
        begin_date = end_date - datetime.timedelta(hours=1)
        
        # Format dates as ISO 8601
        fmt = "%Y-%m-%dT%H:%M:%SZ"
        
        params = {
            "SessionId": self.token,
            "departmentId": department_id,
            "meterId": main_meter_id,
            "beginDate": begin_date.strftime(fmt),
            "endDate": end_date.strftime(fmt),
            "api_key": settings.ABYSIS_API_KEY
        }

        headers = {}
        if settings.ABYSIS_API_KEY:
            headers["api_key"] = settings.ABYSIS_API_KEY

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/Indexes/IndexValuesMatrix", 
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error fetching matrix data: {e}")
                if hasattr(e, 'request'):
                     print(f"Request URL: {e.request.url}")
                raise

abysis_client = AbysisClient()
