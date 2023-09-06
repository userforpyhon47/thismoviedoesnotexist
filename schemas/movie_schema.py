from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime as dt


class Movie(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = Field(min_length=4, max_length=50, default="Hi there")
    category: Optional[str] = Field(default="Category Here")
    description: Optional[str] = Field(default="Description Here")
    year: Optional[int] = Field(ge=1900, le=dt.now().year, default=2000)
    rating: Optional[float] = Field(le=10, ge=0, default=0)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "description": "Descripción de la película",
                "year": 2022,
                "rating": 7.5,
                "category" : "Acción"
            }
        }