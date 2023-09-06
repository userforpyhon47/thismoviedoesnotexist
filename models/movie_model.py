from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database.database_config import Base


class Movie(Base):
    __tablename__ = "Movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    category = Column(String(255), nullable=False, index=True)
    description = Column(String(255), nullable=False, default="Description Here")
    year = Column(Integer, nullable=False, default=1900)
    rating = Column(Float, nullable=False, default=0.0)

   # items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "Items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="items")