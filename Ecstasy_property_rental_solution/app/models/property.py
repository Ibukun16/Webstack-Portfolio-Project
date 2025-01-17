#!/usr/bin/python3
"""Module that holds the Property class"""
import models
from models.base_model import BaseModel, Base
import os
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Property_Type(BaseModel, Base):
    """Representation of the Property class"""
    if models.storage_t == 'db':
        __tablename__ = 'Property_Type'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializing the Property class"""
        super().__init__(*args, **kwargs)
