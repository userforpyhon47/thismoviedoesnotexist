from jwt import encode, decode
import os


def create_token(data: dict={"user_name": "user_login_key"}) -> str:
    """Function to generate jwt token when reciving user_name and user_login_key"""
    return encode(payload=data, key=os.getenv("JWT_KEY"), algorithm="HS256")


def validate_token(jwt_token: str = None) -> dict:
    """Function to convert token to data"""
    data = decode(jwt=jwt_token, key=os.getenv("JWT_KEY"), algorithm=["HS256"])
    return data
