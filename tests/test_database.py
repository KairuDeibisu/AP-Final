import unittest
from tests import DEFAULT_TEST_FILE_PATH
from Note.database import NoteDatabase
from Note.table import Note


class TestNoteDatabase(unittest.TestCase):

    db = NoteDatabase.get_database()

    def test_insert_note(self):
        """
        note is added into database
        """

        note = Note(file=DEFAULT_TEST_FILE_PATH)
        note_id = self.db.insert_note(note)

        self.assertEqual(type(note_id), int)

    def test_read_all_notes(self):
        """
        list of note objects are returned
        """

        notes = self.db.read_all_notes()

        for note in notes:
            self.assertIsInstance(note, Note)

    def test_read_note(self):
        """
        note is returned with id
        """

        note_id = 1

        note = Note(note_id=note_id)

        note = self.db.read_note(note)

        message = f"{note_id} != {note}"

        self.assertTrue(note == None or note_id == note.get_id(), message)

    def test_delete_note(self):
        """
        Delete note from database
        """

        notes = list(self.db.read_all_notes())

        if len(notes) <= 0:
            self.skipTest("No notes to delete")

        note = notes[-1]
        self.db.delete_note(note)
        self.assertEqual(self.db.read_note(note), None)


if __name__ == "__main__":
    unittest.main()
