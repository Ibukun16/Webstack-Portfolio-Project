#!/usr/bin/env python3
"""
Module that contains the BaseModel class
"""


import models
import uuid
import sqlalchemy
from os import getenv
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

time = "%Y-%m-%dT%H:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    """"The Basemodel class from which other classes are derived"""
    if models.storage_t == 'db':
        id = Column(String(60), primary_key=True)
        created_at = Colum(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initializing the base model class"""
        if kwargs:
            for key, val in kwargs.items():
                if key != "__class__":
                    setattr(self, key, val)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__.name__, self.id,
                                         self.__dict__)

    def save(self):
        """Updating the 'updated_at' attribute with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        """Function that a retirns a dictionary conatining all key/value pairs
        of the instance
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["updated_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def delete(self):
        """Function that delet the current instance from the storage"""
        models.storage.delete(self)
