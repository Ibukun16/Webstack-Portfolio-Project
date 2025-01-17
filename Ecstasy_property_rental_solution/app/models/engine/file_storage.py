#!/usr/bin/env python3
"""Module that Contains the FileStorage class
"""

import json
import models
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
        "BaseModel": BaseModel,
        "City": City,
        "Property_Type": Property_Type,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
}


class FileStorage:
    """class function that serializes instances to a JSON file
    & deserializes back to instances
    """
    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty dictionary at creation but will store objects by <class name>.id
    __objects = {}


    def all(self, cls=None):
        """returns a dictionary containing __objects"""
        if cls is not None:
            new_dict = {}
            for key, val in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = val
            return new_dict
        return self.__objects

    def new(self, obj):
        """Function that set the obj with key <obj class name>.id in __objects"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Function that serializes __objects to a JSON file (path: __file_path)"""
        json_objs = {}
        for key in self.__objects:
            if key == "password":
                json_objs[key].decode()
            json_objects[key] = self.__objects[key].to_dict(save_fs=1)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objs, f)

    def reload(self):
        """Function that deserializes a JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                json_load = json.load(f)
            for key in json_load:
                self.__objects[key] = model_classes[json_load[key]["__class__"]](**json_load[key])
        except Exceptions:
            pass

    def delete(self, obj=None):
        """Delete object from __objects if it's inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Function that call reload() method to handle deserialization of json
        file to the objects
        """
        self.reload()

    def get(self, cls, id):
        """Function that returns an object based on the class name and its ID, or
        return None if not found
        """
        if cls not in model_classes.values():
            return None

        all_cls = models.storage.all(cls)
        for val in all_cls.values():
            if (val.id == id):
                return val

        return None

    def count (self, cls=None):
        """Function that count the number of objects in a storage
        """
        all_cls = model_classes.values()

        if not cls:
            count = 0
            for c in all_cls:
                count += len(models.storage.all(c).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
