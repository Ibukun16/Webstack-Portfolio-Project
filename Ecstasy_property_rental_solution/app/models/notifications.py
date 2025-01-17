#!/usr/bin/env python3
"""Module that handle notification messages
"""
import os
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Notification(BaseModel, Base):
    """Function that represent the Notification class"""
    if models.storage_t == 'db':
        __tablename__ = 'Notifications'
        id = Column(String(36), primary_key=True)
        name = Column(String(128), index=True)
        User_id = Column(String(60), ForeignKey('Users.id'), index=True, nullable=False)
        timestamp = Column(Float, index=True, default=time)
        text = Column(String(1024), nullable=False)
        user = relationship('User', back_populates='notifications')
    else:
        id = ""
        name = ""
        User_id = ""
        timestamp = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """Initializing the Notifications class"""
        super().__init__(*args, **kwargs)
