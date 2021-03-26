import unittest
import datetime
from Note.database import NoteDatabase
from Note.table import Note, Tag


class TestNote(unittest.TestCase):

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
        self.assertIsInstance(note.get_content_string(), str)

    def test_str(self):
        """
        Str and Repr override
        """
        path = "test.txt"
        note = Note(file=path)

        try:
            self.assertNotEqual(len(repr(note)), 0)
            self.assertIsInstance(str(note), str)
        except TypeError as e:
            self.fail(e)

    def test_equal(self):
        """
        Does note == equal note use the notes id
        """

        note1 = Note(note_id=1)
        note2 = Note(note_id=1)
        note3 = Note(note_id=3)

        self.assertTrue(note1 == note2)
        self.assertTrue(note1 != note3)
        self.assertTrue(note2 == note1)
        self.assertTrue(note2 != note3)


if __name__ == "__main__":
    unittest.main()
