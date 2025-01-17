#!/usr/bin/env python3
"""Module that handles the DBStorage class
"""


import models
import sqlalchemy
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.property import Property_Type
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


model_classes = {
        "Amenity": Amenity,
        "City": City,
        "Property_Type": Property_Type,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
}


class DBStorage:
    """class to interact with the MySQL database."""
    __engine = None
    __session = None


    def __init__(self):
        """Instatiating the DBStorage object"""
        E_MYSQL_USER = getenv('Ecstasy_MYSQL_USER')
        E_MYSQL_PWRD = getenv('Ecstasy_MYSQL_PWRD')
        E_MYSQL_HOST = getenv('Ecstasy_MYSQL_HOST')
        E_MYSQL_DB = getenv('Ecstasy_MYSQL_DB')
        E_ENV = getenv('Ecstasy_ENV')
        self.__engine = create_engine(
        f'mysql+mysqldb://{E_MYSQL_USER}:{E_MYSQL_PWRD}@{E_MYSQL_HOST}/{E_MYSQL_DB}')
        if E_ENV == "test":
            Base.metadata.drop_all(self.__engine)

def all(self, cls=None):
    """Query for the current database session"""
    new_dict = {}
    for clss in model_classes:
        if cls is None or cls in model_classes[clss] or cls is clss:
            objs = self.__session.query(model_classes[clss]).all()
            for obj in objs:
                key = obj.__class__.__name__+ '.' + obj.id
                new_dict[key] = obj
    return (new_dict)

def new(self, obj):
    """Add an object to the current database session"""
    self.__session.add(obj)

def save(self):
    """commit all changes made to the current database session"""
    self.__session.commit()

def delete(self, obj=None):
    """Delete object from the current database session obj else None"""
    if obj is not None:
        self.__session.delete(obj)

def reload(self):
    """Reloads data from the database"""
    Base.metadata.create_all(self.__engine)
    sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
    Session =scoped_session(sess_factory)
    self.__session = Session

def close(self):
    """call remove() method on the private session attribute"""
    self.__session.remove()

def get(self, cls, id):
    """function that retrieves an object based on the class name and its ID,
    or return None if not found
    """
    if cls not in model_classes.values():
        return None

    all_cls = models.storage.all(cls)
    for val in all_cls.values():
        if (val.id == id):
            return val

    return None

def count(self, cls=None):
    """Count the number of object in the storage
    """
    all_cls = models_classes.values()

    if not cls:
        count = 0
        for c in all_cls:
            count += len(models.storage.all(c).values())

    return count
