
#Third party imports
from fastapi import APIRouter
from fastapi import Path, Query, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Union


# Custom imports
from utils.env_manager import load_credentials
load_credentials()

from schemas.movie_schema import Movie as MovieSchema
from middleware.jwt_validator import JWT_Bearer
from database.database_config import SessionLocal
from models.movie_model import Movie as MovieModel
from services.movie_service import MovieService



# Create instance of APIrouter
movie_router = APIRouter()


# Endpoint to get all movies
@movie_router.get("/movies", tags=["Movies"], response_model=List[MovieSchema], status_code=status.HTTP_200_OK)
def get_movies() -> List[MovieSchema]:
    """Endpoint to get all movies
    Successful response contains a empty list or a list of movies"""
    return MovieService(SessionLocal()).get_movies()

# Endpoint to get movie by id
@movie_router.get("/movies/{movie_id}", tags=["Movies"], response_model=MovieSchema, status_code=status.HTTP_200_OK)
def get_movie_by_id(movie_id: int = Path(ge=0, le=10)) -> MovieSchema:
    """Endpoint to get a movie by id using parameter movie_id
    Successful response contains a Movie"""
    return MovieService(SessionLocal()).get_movie_by_id(movie_id)
    

# Endpoint to search movie by category name
@movie_router.get("/movies/", tags=["Movies"], response_model=List[MovieSchema])
def search_movies_by_category(category_name: str = Query(min_length=5, max_length=15)) -> List[MovieSchema]:
    return MovieService(SessionLocal()).search_movies_by_category(category_name)


# Enpoint to create a movie
@movie_router.post("/movies/add", tags=["Movies"], response_model=dict, status_code=status.HTTP_200_OK)
def post_movie(movie: MovieSchema) -> dict:
    return MovieService(SessionLocal()).post_movie(movie)


# Endpoint to delete a movie
@movie_router.delete("/movies/delete/{movie_id}", tags=["Movies"], response_model=Union[MovieSchema, dict])
def delete_movie(movie_id: int) -> MovieSchema | dict:
    return MovieService(SessionLocal()).delete_movie(movie_id)


# Endpoint to update a movie
@movie_router.put("/movies/update/{movie_id}", tags=["Movies"], response_model=Union[MovieSchema, dict], status_code=status.HTTP_200_OK)
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

