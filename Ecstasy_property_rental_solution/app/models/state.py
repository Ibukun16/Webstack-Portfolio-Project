#!/uar/bin/env python3
"""Module that handles the State function"""
import models
import sqlalchemy
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Function that represent the state class"""
    if models.storage_t == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        Cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""


    def __init__(self, *args, **kwargs):
        """Initializing the state class"""
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def cities(self):
            """Getter function that retrieves the list of city instances related to
            the state"""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
