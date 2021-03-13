from tests import DEFAULT_TEST_FILE_PATH
import unittest
from Note.database import NoteDatabase
from Note.table import Note


class TestNoteDatabase(unittest.TestCase):

    db = NoteDatabase.get_database()

    def test_insert_note(self):
        """
        note is added into database
        """

        note = self.get_test_note_object()
        note_id = self.db.insert_note(note)

        self.assertEqual(type(note_id), int)

    def test_get_all_notes(self):
        """
        list of note objects are returned
        """

        notes = self.db.get_all_notes()

        for note in notes:
            self.assertIsInstance(note, Note)

    def test_search_by_id(self):
        """
        note is returned with id
        """

        note_id = 1

        note = self.db.get_note_by_id(note_id)

        message = f"{note_id} != {note}"

        self.assertTrue(note == None or note_id == note.get_id(), message)

    def test_delete_note(self):
        """
        Delete note from database
        """
        notes = list(self.get_all_notes())

        if len(notes) <= 0:
            self.skipTest("No notes to delete")

        note = notes[-1].get_id()
        self.db.delete_note(note)
        self.assertEqual(self.db.get_note_by_id(note), None)

    def get_all_notes(self):
        return self.db.get_all_notes()

    def get_test_note_object(self):
        return Note(content=Note.file_to_binary(DEFAULT_TEST_FILE_PATH))
