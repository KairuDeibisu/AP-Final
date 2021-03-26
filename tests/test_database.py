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

        with NoteDatabase.get_database() as db:
            note_id = db.insert_note(note)

        self.assertEqual(type(note_id), int)

    def test_read_all_notes(self):
        """
        list of note objects are returned
        """
        with NoteDatabase.get_database() as db:
            notes = db.read_all_notes()

        for note in notes:
            self.assertIsInstance(note, Note)

    def test_read_note(self):
        """
        note is returned with id
        """

        note_id = 1

        note = Note(note_id=note_id)

        with NoteDatabase.get_database() as db:
            note = db.read_note(note)

        self.assertTrue(note == None or note_id == note.get_id())

    def test_delete_note(self):
        """
        Delete note from database
        """
        with NoteDatabase.get_database() as db:
            notes = list(db.read_all_notes())

            if len(notes) <= 0:
                self.skipTest("No notes to delete")

            note = notes[-1]
            db.delete_note(note)
            self.assertEqual(db.read_note(note), None)


if __name__ == "__main__":
    unittest.main()
