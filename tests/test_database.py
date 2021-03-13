import unittest
from Note.database import NoteDatabase
from Note.table import Note


class TestNoteDatabase(unittest.TestCase):
    db = NoteDatabase.get_database()

    def test_search_by_id(self):
        """
        note is returned with id
        """

        note_id = 1

        note = self.db.get_note_by_id(note_id)

        self.assertEqual(note_id, note.get_id())

    def test_get_all_notes(self):
        """
        list of note objects are returned
        """

        notes = self.db.get_all_notes()

        for note in notes:
            self.assertIsInstance(note, Note)
