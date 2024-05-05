#!/usr/bin/python3
"""a module that tests Amenity class"""
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity

import MySQLdb
from os import getenv

# host = getenv('HBNB_MYSQL_HOST')
# user = getenv('HBNB_MYSQL_USER')
# password = getenv('HBNB_MYSQL_PWD')
# mydb = getenv('HBNB_MYSQL_DB')

# db = MySQLdb.connect(host='localhost', user=user, password=password, db=mydb)
# cur = db.cursor()


class test_Amenity(test_basemodel):
    """a class that tests amentiy"""

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
