#Third party imports
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


# Custom imports
from utils.env_manager import load_credentials
load_credentials()
from jwt_manager import create_token
from schemas.user_schema import User


# Create instance of APIrouter
user_router = APIRouter()


# Endpoint for user to login
@user_router.post("/users", tags=["Users"], response_model=dict, status_code=status.HTTP_200_OK)
def login(user: User) -> dict:
    if user.login == "test" and user.passwd == "test":
        return JSONResponse(content={"token": create_token(user.model_dump())})
    else:
        return JSONResponse(content={"Result": "Incorrect login/password"}, status_code=status.HTTP_401_UNAUTHORIZED)
