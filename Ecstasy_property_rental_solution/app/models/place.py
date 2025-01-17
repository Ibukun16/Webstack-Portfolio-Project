#!/usr/bin/env python3
"""Module that handles the Place class"""
import os
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

if models.storage_t = 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id', onupdate=ondelete='CASCADE'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id', onupdate='CASCADE',
                                            ondelete='CASCADE'), primary_key=True)
                          Column('property_type_id', String(60),
                                 ForeignKey('property.id', onupdate=ondelete'CASCADE')


class Place(BaseModel, Base):
    """Function that represent the Place class"""
    if models.storage_t == 'db':
        __tablename__ = 'Places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_of_rooms = Column(Integer, nullable=False, default=0)
        number_of_bathrooms = Column(Integer, nullable=False, default=0)
        max_occupants = Column(Integer, nullable=False, default=0)
        number_of_toilets = Column(Integer, nullable=False, default=0)
        kitchen_type = Column(String(60), nullable=False)
        swimming_pool = Column(String(60), nullable=False)
        sewage_treatment = Column(Boolean, nullable=False)
        water_treatment = Column(Boolean, nullable=False)
        access_control = Column(Boolean, nullable)
        dimensional details = Column(String(700), nullable=False)
        payment_condition = Column(String(60), nullable=False)
        security_features = Column(String(400), nullable=False)
        other_features = Column(String(400), nullable=True)
        usage = Column(String(60), nullable=False)
        location = Column(String(120), nullable=True)
        price = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)
        property_type = relationship("Property_Type", secndary

    else:
        city_id=""
        user_id = ""
        name = ""
        description = ""
        number_of_rooms = 0
        number_of_bathrooms = 0
        max_occupants = 0
        number_of_toilets = 0
        kitchen_type = ""
        swimming_pool = ""
        sewage_treatment = ""
        water_treatment = ""
        access_control = ""
        dimensional_details = ""
        payment_condition = ""
        security_features = ""
        other_features = ""
        location = ""
        usage = ""
        price = 0
        latitude = ""
        longitude = ""
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initializing the Place class"""
        super().__init__(*args, **kwargs)


    if models.storage_t != 'db':
        @property
        def reviews(self):
            """Getter function that retrieves the list of Review instances"""
        from models.review import Review
        review_list = []
        all_reviews = models.storage.all(Review)
        for review in all_reviews.values():
            if review.place_id == self.id:
                review_list.append(review)
        return review_list

    @property
    def amenities(self):
        """Getter function that retrieves the list of Amenity instances"""
        from models.amenity import Amenity
        amenity_list = []
        all_amenities = models.storage.all(Amenity)
        for amenity in all_amenities.values():
            if amenity.place_id == self.id:
                amenity_list.append(amenity)
        return amenity_list
