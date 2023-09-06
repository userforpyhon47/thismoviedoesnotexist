from fastapi.security import HTTPBearer
from fastapi import Request, status, HTTPException

class JWT_Bearer(HTTPBearer):
    """Class used to validate JWT_token"""
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        print(auth.credentials)
        if auth.credentials != "ABC":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        