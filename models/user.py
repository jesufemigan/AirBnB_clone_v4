#!/usr/bin/python3
"""This module defines a class User"""
import hashlib
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", backref="user", cascade="all, delete")
    reviews = relationship("Review", backref="user", cascade="all, delete")
    if storage_type != 'db':
        password = ""

    def __init__(self, *args, **kwargs):
        """initialize for password hash"""
        if 'password' in kwargs:
            password = kwargs['password']
            password_hash = self.generate_hash_password(password)
            kwargs['password'] = password_hash
        super().__init__(*args, **kwargs)

    @staticmethod
    def generate_hash_password(password):
        """generate hashed password"""
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.md5(password_bytes)
        return hash_object.hexdigest()
