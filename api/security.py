from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

API_SECRET_KEY = "your-secret-key"
API_KEY_NAME = "X-API-Key"  # or any custom header name you want

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
