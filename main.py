#built in import
import os
import openai

#Third party imports
from fastapi import FastAPI, Path, Query, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Union

# Custom imports
from env_manager import load_credentials
load_credentials()

from jwt_manager import create_token
from schemas.movie_schema import Movie as MovieSchema
from schemas.user_schema import User

from middleware.jwt_validator import JWT_Bearer
from middleware.error_handler import ErrorHandler
from database.database_config import engine, Base, SessionLocal
from models.movie_model import Movie as MovieModel

app = FastAPI(title="This Movie Doesn´t exist",
              description="A simple API that leverages chatGPT and Dalle \
                generative AIs to create a movie catalog",
              version="0.1")

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)


@app.post("/users", tags=["Users"], response_model=dict, status_code=status.HTTP_200_OK)
def login(user: User) -> dict:
    
    if user.login == "test" and user.passwd == "test":
        return JSONResponse(content={"token": create_token(user.model_dump())})
    else:
        return JSONResponse(content={"Result": "Incorrect login/password"}, status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/movies", tags=["Movies"], response_model=List[MovieSchema], status_code=status.HTTP_200_OK)
def get_movies() -> List[MovieSchema]:
    """Endpoint to get all movies
    Successful response contains a Movie"""
    try:
        db = SessionLocal()
        result = db.query(MovieModel).limit(limit=3).all()
    except Exception as exc:
        return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JSONResponse(content=jsonable_encoder(result))


@app.get("/movies/{movie_id}", tags=["Movies"], response_model=MovieSchema, status_code=status.HTTP_200_OK)
def get_movie_by_id(movie_id: int = Path(ge=0, le=10)) -> MovieSchema:
    """Endpoint to get a movie by id using parameter movie_id
    Successful response contains a Movie"""
    try:
        db = SessionLocal()
        result = db.query(MovieModel).filter(MovieModel.id==movie_id).first()
        assert result is not None, "Movie doesn´t exist"
    except (Exception, AssertionError) as exc:
        return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        return JSONResponse(content=jsonable_encoder(result))


@app.get("/movies/", tags=["Movies"], response_model=List[MovieSchema])
def search_movies_by_category(category_name: str = Query(min_length=5, max_length=15)) -> List[MovieSchema]:
    try:
        db = SessionLocal()
        result = db.query(MovieModel).filter(MovieModel.category.icontains(category_name)).limit(limit=4).all()
        assert result is not None, "No matching movies"
    except (Exception, AssertionError) as exc:
        return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        return JSONResponse(content=jsonable_encoder(result))

@app.post("/movies/add", tags=["Movies"], response_model=dict, status_code=status.HTTP_200_OK)
def post_movie(movie: MovieSchema) -> dict:
    try:
        db = SessionLocal()
        db.add(MovieModel(**movie.model_dump()))
        db.commit()
    except Exception as exc:
        return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JSONResponse(content={"Status": "Succesfully added"})


@app.delete("/movies/delete/{movie_id}", tags=["Movies"], response_model=Union[MovieSchema, dict])
def delete_movie(movie_id: int) -> MovieSchema | dict:
    try:
        db = SessionLocal()
        result = db.query(MovieModel).filter(MovieModel.id==movie_id).first()
        assert result is not None, "Movie doesn´t exist"
        db.delete(result)
        db.commit()
    except (Exception, AssertionError) as exc:
        return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        return JSONResponse(content=jsonable_encoder(result))


@app.put("/movies/update/{movie_id}", tags=["Movies"], response_model=Union[MovieSchema, dict], status_code=status.HTTP_200_OK)
def update_movie(movie_id: int, movie: MovieSchema) -> MovieSchema | dict:
    try:
        db = SessionLocal()
        result = db.query(MovieModel).filter(MovieModel.id==movie_id).first()
        assert result is not None, "Movie doesn´t exist"
        result.category = movie.category
        db.commit()
    except (Exception, AssertionError) as exc:
        return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        return JSONResponse(content=jsonable_encoder(result))

# openai.organization = os.getenv("OPENAI_ORG_ID")
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.Model.list()