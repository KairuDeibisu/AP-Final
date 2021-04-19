import unittest

from Note.database.database import NoteDatabase
from Note.database.database import Database as ImplementedDatabase

class Database:
    pass

class TestNoteDatabase(unittest.TestCase):

    def test_init_database(self):
        """
        The database can be created without error.
        """

        db = NoteDatabase(Database)
        
        self.assertIsInstance(db, NoteDatabase)

class TestDatabase(unittest.TestCase):

    def test_singleton(self):
        """
        The database only has one instance
        """

        self.assertIsNone(ImplementedDatabase._instance)

        db_instace_1 = ImplementedDatabase()
        db_instace_1_obj = id(db_instace_1)

        self.assertIsNotNone(ImplementedDatabase._instance)

        db_instace_2 = ImplementedDatabase()
        db_instace_2_obj = id(db_instace_2)


        self.assertIsInstance(db_instace_1, ImplementedDatabase)
        self.assertIsInstance(db_instace_2, ImplementedDatabase)
        
        self.assertEqual(db_instace_1_obj, db_instace_2_obj)
