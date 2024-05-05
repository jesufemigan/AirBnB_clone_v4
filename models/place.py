#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
import os
import models


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             nullable=False, primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             nullable=False, primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    name = Column(String(128), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place",
                            cascade="all, delete")
    amenities = relationship(
        "Amenity", secondary="place_amenity", viewonly=False)
    amenity_ids = []
    
    if models.storage_type != "db":
        @property
        def reviews(self):
            """getter attribute for reviews"""
            from models import storage
            from models.review import Review
            all_reviews = storage.all(Review)
            reviews_with_place_id = []
            for review in all_reviews.values():
                if review['review_id'] == self.id:
                    reviews_with_place_id.append(review)
            return reviews_with_place_id

        @property
        def amenities(self):
            """getter property for amenities"""
            from models import storage
            from models.amenity import Amenity
            all_amenites = storage.all(Amenity)
            amenities_linked_with_place = []
            for amenity_id in self.amenity_ids:
                for amenity in all_amenites.values():
                    if amenity_id == amenity.id:
                        amenities_linked_with_place.append(amenity)
            return amenities_linked_with_place

        @amenities.setter
        def amenities(self, value):
            """sets amenities"""
            from models.amenity import Amenity
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
