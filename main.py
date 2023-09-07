#Third party imports
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import openai


# Custom imports
from utils.env_manager import load_credentials
load_credentials()


from routers.movie_router import movie_router
from routers.user_router import user_router


from middleware.error_handler import ErrorHandler
from database.database_config import engine, Base

app = FastAPI(title="This Movie Doesn´t exist",
              description="A simple API that leverages chatGPT and Dalle \
                generative AIs to create a movie catalog",
              version="0.1")

app.add_middleware(ErrorHandler) # Add middlware error handle to handle exceptions
app.include_router(movie_router) #Add router for movies endpoints
app.include_router(user_router) #Add router for user endpoints
Base.metadata.create_all(bind=engine) #Create all tables is database


# openai.organization = os.getenv("OPENAI_ORG_ID")
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.Model.list()