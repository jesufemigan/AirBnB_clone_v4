#!/usr/bin/python3
"""a module that tests dbstorage"""
import unittest
import MySQLdb
import models
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine.db_storage import DBStorage
from os import getenv


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'NO DB')
class TestDBStorage(unittest.TestCase):
    """a class that tests db storage"""
    @classmethod
    def setUpClass(self):
        """set up test"""
        self.User = getenv("HBNB_MYSQL_USER")
        self.Passwd = getenv("HBNB_MYSQL_PWD")
        self.Db = getenv("HBNB_MYSQL_DB")
        self.Host = getenv("HBNB_MYSQL_HOST")
        self.db = MySQLdb.connect(host=self.Host, user=self.User,
                                  password=self.Passwd, db=self.Db)
        self.cur = self.db.cursor()
        self.storage = DBStorage()
        self.storage.reload()

    @classmethod
    def teardown(self):
        """tear down at end"""
        self.cur.close()
        self.db.close()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_read_tables(self):
        """show existing tables"""
        self.cur.execute("SHOW TABLES")
        table_count = self.cur.fetchall()
        self.assertEqual(len(table_count), 7)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_empty_tables_amenities(self):
        """check if amenities is empty at inception"""
        self.cur.execute("SELECT * FROM amenities")
        amenities = self.cur.fetchall()
        self.assertEqual(len(amenities), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_empty_tables_cities(self):
        """check if cities is empty at inception"""
        self.cur.execute("SELECT * FROM cities")
        cities = self.cur.fetchall()
        self.assertEqual(len(cities), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_empty_tables_places(self):
        """check if places is empty at inception"""
        self.cur.execute("SELECT * FROM places")
        places = self.cur.fetchall()
        self.assertEqual(len(places), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_empty_tables_states(self):
        """check if states is empty at inception"""
        self.cur.execute("SELECT * FROM states")
        states = self.cur.fetchall()
        self.assertEqual(len(states), 1)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_empty_tables_users(self):
        """check if users is empty at inception"""
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        self.assertEqual(len(users), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_add_new_state(self):
        """test to check if new state is added"""
        self.cur.execute("SELECT * FROM states")
        states = self.cur.fetchall()
        self.assertEqual(len(states), 0)
        state = State(name="Lagos")
        state.save()
        self.db.autocommit(True)
        self.cur.execute("SELECT * FROM states")
        states = self.cur.fetchall()
        self.assertEqual(len(states), 1)
        
    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_get_method(self):
        """test to check if object is being retrieved based on id"""
        state = State(name="Alabama")
        state.save()
        created_state = models.storage.get(State, state.id)
        self.assertEqual(state, created_state)
    
    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_count_method(self):
        """test to check if object is being retrieved based on id"""
        self.assertEqual(len(models.storage.all()), models.storage.count())
        


if __name__ == '__main__':
    unittest.main()
