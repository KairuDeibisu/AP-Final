import unittest

from Note.database.database import NoteDatabase


class TestNoteDatabase(unittest.TestCase):

    def test_init_database(self):
        """
        The database can be created without error.
        """

        db = NoteDatabase()
