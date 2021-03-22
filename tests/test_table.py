import unittest
import datetime
from Note.database import NoteDatabase
from Note.table import Note, Tag


class TestNote(unittest.TestCase):
    db = NoteDatabase.get_database()

    def test_create_note(self):
        """
        Create from file
        """
        path = "test.txt"
        note = Note(file=path)

        with open(path, "r") as f:
            data = f.read()

        self.assertEqual(note.get_content(), data.encode())
        self.assertIsInstance(note.get_date(), datetime.date)

    def test_get_content(self):
        """
        Get note content is bytes object
        """
        path = "test.txt"
        note = Note(file=path)

        self.assertIsInstance(note.get_content(), bytes)

    def test_str(self):
        path = "test.txt"
        note = Note(file=path)

        try:
            self.assertNotEqual(len(repr(note)), 0)
            self.assertIsInstance(str(note), str)
        except TypeError as e:
            self.fail(e)


if __name__ == "__main__":
    unittest.main()
