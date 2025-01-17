#!/usr/bin/python3
"""
A module that initializes the models package 
"""
import os

storage_t = os.getenv("ECSTASY_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
