#!/usr/bin/env python3
"""Module that handles the City class"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Function that represent the City class"""
    if models.storage_t == "db":
        __tablename__ = 'Cities'
        state_id = Column(String(60), ForeignKey('States.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="Cities",
                              cascade="all, delete, delete-orphan")

    else:
        state_id = ""
        name = ""


    def __init__(self, *args, **kwargs):
        """Initializing the city class"""
        super().init__(*args, **kwargs)


    if models.storage_t != 'db':
        @property
        def property_type(self):
        """Getter function that retrieves the list of all Property instances
        from a city
        """
        from models.property import Property_Type
        property_list = []
        all_properties = models.storage.all(Property_Type)
        for propty in all_properties.values():
            if propty.city_id == self.id:
                property_list.append(propty)
        return property_list
