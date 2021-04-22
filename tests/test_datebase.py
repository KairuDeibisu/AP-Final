

from Note.database.database import NoteDatabase
from Note.database.database import Database

from Note.database.table import Note, Tag

import unittest

from faker import Faker


Database._db_path = "test.db"


class TestDatabase(unittest.TestCase):

    def test_singleton(self):
        """
        The database only has one instance.
        """

        self.assertIsNone(Database._instance)

        db_instace_1 = Database()

        db_instace_1_obj = id(db_instace_1)

        self.assertIsNotNone(Database._instance)

        db_instace_2 = Database()
        db_instace_2_obj = id(db_instace_2)

        self.assertIsInstance(db_instace_1, Database)
        self.assertIsInstance(db_instace_2, Database)

        self.assertEqual(db_instace_1_obj, db_instace_2_obj)


class TestNoteDatabase(unittest.TestCase):

    def test_init_database(self):
        """
        The database can be created without error.
        """

        db = NoteDatabase(Database)

        self.assertIsInstance(db, NoteDatabase)
    
    def test_common_element_in_lists(self):
        """
        Can find the commen element of n number of lists.
        """
        lists = [
            [2,3,4,5],
            [1,3,4,5],
            [1,2,4,5]
        ]

        db = NoteDatabase(Database)

        self.assertFalse(db._common_element_in_lists(lists, 1))
        self.assertFalse(db._common_element_in_lists(lists, 2))
        self.assertFalse(db._common_element_in_lists(lists, 3))

        self.assertTrue(db._common_element_in_lists(lists, 4))
        self.assertTrue(db._common_element_in_lists(lists, 5))

    def test_insert_note(self):
        """
        Notes can be inserted into the database.
        """

        fake = Faker()

        db = NoteDatabase(Database)

        date_ = fake.future_date()

        notes = [
            Note(content=fake.text(10).encode("utf-8")),
            Note(content=fake.text(10).encode("utf-8"), active=False),
            Note(content=fake.text(10).encode("utf-8"), date_=date_),
            Note(content=fake.text(10).encode("utf-8"), date_=date_),
        ]

        for note in notes:
            db.insert_note(note)

        self.assertTrue(db.last_row_id)

    def test_select_note(self):
        """
        Can select note from database.
        """
        fake = Faker()

        db = NoteDatabase(Database)

        note = Note(content=fake.text(10).encode("utf-8"))

        db.insert_note(note)

        note = db.select_note(db.last_row_id)

        self.assertIsInstance(note, Note)
        self.assertIsNotNone(note.id_)
        self.assertIsNotNone(note.date_)
        self.assertIsNotNone(note.content)
        self.assertIsNotNone(note.active)

    def test_delete_note(self):
        """
        Make sure note can be deleted from database.
        """

        fake = Faker()

        db = NoteDatabase(Database)

        note = Note(content=fake.text(10).encode("utf-8"))

        db.insert_note(note)

        db.delete_note(db.last_row_id)

        note = db.select_note(db.last_row_id)

        self.assertFalse(note)

    def test_remove_note(self):
        """
         Make sure note can be removed from database.
        """

        fake = Faker()

        db = NoteDatabase(Database)

        note = Note(content=fake.text(10).encode("utf-8"))

        db.insert_note(note)

        note = db.select_note(db.last_row_id)

        db.remove_note(note.id_)

        note = db.select_note(db.last_row_id)

        self.assertIsNotNone(note)
        self.assertFalse(note.active)
        

    def test_select_note_by_tag(self):
        """
        Can select note by tags.
        """

        fake = Faker()

        notes_to_insert = [
            Note(content=fake.text(10).encode("utf-8")),
            Note(content=fake.text(10).encode("utf-8")),
            Note(content=fake.text(10).encode("utf-8")),
            Note(content=fake.text(10).encode("utf-8")),
        ]

        tags_to_insert = [
            ["test"],
            ["dev"],
            ["test", "dev"],
            ["dev", "test"]
        ]

        db = NoteDatabase(Database)

        for note in notes_to_insert:
            db.insert_note(note)
        
        inserted_notes = [db.select_note(db.last_row_id - i) for i in range(len(notes_to_insert))]        
        inserted_notes.reverse()

        for i,note in enumerate(inserted_notes):
            tags = [Tag(fk_note_id=note.id_,name=tag) for tag in tags_to_insert[i]]
            db.insert_tag(tags)
        
        matches = db.select_note_by_tags(["test"])
        matches = [note.id_ for note in matches]
        self.assertIn(inserted_notes[0].id_, matches)
        self.assertIn(inserted_notes[2].id_, matches)
        self.assertIn(inserted_notes[3].id_, matches)

        matches = db.select_note_by_tags(["dev"])
        matches = [note.id_ for note in matches]
        self.assertIn(inserted_notes[1].id_, matches)
        self.assertIn(inserted_notes[2].id_, matches)
        self.assertIn(inserted_notes[3].id_, matches)

        matches = db.select_note_by_tags(["test","dev"])
        matches = [note.id_ for note in matches]
        self.assertNotIn(inserted_notes[0].id_, matches)
        self.assertNotIn(inserted_notes[1].id_, matches)
        self.assertIn(inserted_notes[2].id_, matches)
        self.assertIn(inserted_notes[3].id_, matches)

        matches = db.select_note_by_tags([])
        self.assertFalse(matches)
            