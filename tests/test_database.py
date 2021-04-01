import unittest
from tests import DEFAULT_TEST_FILE_PATH
from Note.database import NoteDatabase
from Note.request import NoteRequest
from Note.table import Note


class TestNoteDatabase(unittest.TestCase):

    db = NoteDatabase.get_database()

    def test_read(self):
        """
        Notes can be read from database
        """

        with NoteDatabase.get_database() as db:

            limit = 5

            request = NoteRequest(limit=limit)
            notes_list = db.read(request)

            if n := len(notes_list) <= 0:
                self.skipTest("No notes to read")

            self.assertLessEqual(n, limit)
            for note in notes_list:
                self.assertTrue(isinstance(note, Note))

    def test_create(self):
        """
        Notes can be create in the database
        """
        note = Note(file=DEFAULT_TEST_FILE_PATH)

        with NoteDatabase.get_database() as db:

            content = note.get_content()
            request = NoteRequest(content=content)

            ID = db.create(request)

            request = NoteRequest(ID=ID)

            note, = db.read(request)

            self.assertEqual(note.get_id(), ID)
            self.assertEqual(note.get_content(), content)

    def test_update(self):
        """
        Notes in the database can be updated
        """
        note = Note(file=DEFAULT_TEST_FILE_PATH)

        with NoteDatabase.get_database() as db:
            request = NoteRequest(content=note.get_content())

            ID = db.create(request)

            request = NoteRequest(ID=ID)

            note, = db.read(request)
            note.set_active(False)

            request = NoteRequest(
                ID=note.get_id(),
                content=note.get_content(),
                active=note.get_active())

            db.update(request)

            request = NoteRequest(ID=ID)
            note, = db.read(request)

            self.assertFalse(note.get_active())

    def test_delete(self):
        """
        Notes can be deleted from the database
        """
        with NoteDatabase.get_database() as db:

            request = NoteRequest(limit=5)

            notes_list = db.read(request)

            if len(notes_list) <= 0:
                self.skipTest("No notes to delete")

            note = notes_list[0]

            request = NoteRequest(ID=note.get_id())
            db.delete(request)

            request = NoteRequest(ID=note.get_id())
            notes_list = db.read(request)

            self.assertFalse(notes_list)


if __name__ == "__main__":
    unittest.main()
