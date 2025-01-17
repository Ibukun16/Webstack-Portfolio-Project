#!/usr/bin/python3
"""Module that holds the Amenity class"""
import models
from models.base_model import BaseModel, Base
import os
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Representation of the Amenity class"""
    if models.storage_t == 'db':
        __tablename__ = 'Amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializing the Amenity class"""
        super().__init__(*args, **kwargs)
