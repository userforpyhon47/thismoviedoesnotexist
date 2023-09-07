from database.database_config import SessionLocal
from schemas.movie_schema import Movie as MovieSchema
from models.movie_model import Movie as MovieModel
from fastapi import status
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class MovieService():
    def __init__(self, db: SessionLocal) -> None:
        self.db = db

    def get_movies(self) -> List[MovieSchema]:
        try:
            result = self.db.query(MovieModel).limit(limit=3).all()
        except Exception as exc:
            return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JSONResponse(content=jsonable_encoder(result))

    def get_movie_by_id(self, movie_id: int) -> MovieSchema:
        try:
            result = self.db.query(MovieModel).filter(MovieModel.id==movie_id).first()
            assert result is not None, "Movie doesn´t exist"
        except (Exception, AssertionError) as exc:
            return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_404_NOT_FOUND)
        else:
            return JSONResponse(content=jsonable_encoder(result))
        
    def search_movies_by_category(self, category_name: str) -> List[MovieSchema]:
        try:
            result = self.db.query(MovieModel).filter(MovieModel.category.icontains(category_name)).limit(limit=4).all()
            assert result is not None, "No matching movies"
        except (Exception, AssertionError) as exc:
            return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_404_NOT_FOUND)
        else:
            return JSONResponse(content=jsonable_encoder(result))
    
    def post_movie(self, movie: MovieSchema) -> dict:
        try:
            self.db.add(MovieModel(**movie.model_dump()))
            self.db.commit()
        except Exception as exc:
            return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JSONResponse(content={"Status": "Succesfully added"})
        
    def delete_movie(self, movie_id: int) -> MovieSchema | dict:
        try:
            result = self.db.query(MovieModel).filter(MovieModel.id==movie_id).first()
            assert result is not None, "Movie doesn´t exist"
            self.db.delete(result)
            self.db.commit()
        except (Exception, AssertionError) as exc:
            return JSONResponse(content={"Error": exc.__str__()}, status_code=status.HTTP_404_NOT_FOUND)
        else:
            return JSONResponse(content=jsonable_encoder(result))