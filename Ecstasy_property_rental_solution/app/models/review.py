#!/usr/bin/env python3
"""Module that handles the Review function"""
import models
import sqlalchemy
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Function that represent the the Review class"""
    if models.storage_t == 'db':
        __tablename__ = 'Reviews'
        Place_id = Column(String(60), ForeignKey('Places.id'), nullable=False)
        User_id = Column(String(60), ForeignKey('Users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        Place_id = ""
        User_id = ""
        text = ""


    def __init__(self, *args, **kwargs):
        """Initializing the Review class"""
        super().__init__(*args, **kwargs)
