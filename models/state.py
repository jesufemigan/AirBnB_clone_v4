#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


storage_type = os.getenv('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    # For DB
    cities = relationship("City", backref="state", cascade="all, delete")
    # For FileStorage
    if storage_type != 'db':
        @property
        def cities(self):
            from models import storage
            all_cities = storage.all(City)
            cities_with_state_id = []
            for city in all_cities.values():
                if city.state_id == self.id:
                    cities_with_state_id.append(city)
            return cities_with_state_id
