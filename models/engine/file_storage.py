#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}
    classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            filtered_class = {}
            for key, value in self.__objects.items():
                if value.__class__ == cls:
                    filtered_class[key] = value
            return filtered_class
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = self.classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """deletes obj from __objects"""
        if obj is not None:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]

    def close(self):
        """desrialize JSON file to objects"""
        self.reload()
        
    def get(self, cls, id):
        """retrieves one object""" 
        obj_for_class = {}
        for key, value in self.__objects.items():
            if value.__class__ == cls:
                obj_for_class[key] = value
        for obj in obj_for_class.values():
            if obj.id == id:
                return obj
        return None
    
    def count(self, cls=None):
        """counts number of objects in storage matching given class"""
        cls_obj = self.all(cls)
        return len(cls_obj)
