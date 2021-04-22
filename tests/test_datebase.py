

from Note.database.database import NoteDatabase
from Note.database.database import Database

from Note.database.table import Note

import unittest

from faker import Faker


Database._db_path = "test.db"


class TestDatabase(unittest.TestCase):

    def test_singleton(self):
        """
        The database only has one instance
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
            Note(content=fake.text(10).encode("utf-8"), tags="test"),
            Note(content=fake.text(10).encode("utf-8"), tags="test"),
            Note(content=fake.text(10).encode("utf-8"), tags="dev"),
            Note(content=fake.text(10).encode("utf-8"), tags="dev"),
            Note(content=fake.text(10).encode("utf-8"), tags="test,dev"),
            Note(content=fake.text(10).encode("utf-8"), tags="test,dev"),
            Note(content=fake.text(10).encode("utf-8"), tags="dev,test"),
            Note(content=fake.text(10).encode("utf-8"), tags="dev,test"),
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
        Make sure note can be from database.
        """

        fake = Faker()

        db = NoteDatabase(Database)

        note = Note(content=fake.text(10).encode("utf-8"))

        db.insert_note(note)

        db.delete_note(db.last_row_id)

        note = db.select_note(db.last_row_id)

        self.assertFalse(note)

    def test_remove_note(self):

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

        tag_set_one = ["test"]
        tag_set_two = ["dev"]
        tag_set_three = ["test", "dev"]
        tag_set_four = ["dev", "test"]
        tag_set_five = ["test", "dev", "cat", "bat", "rat"]

        fake = Faker()

        notes = [
            Note(content=fake.text(10).encode("utf-8"), tags="test"),
            Note(content=fake.text(10).encode("utf-8"), tags="test"),
            Note(content=fake.text(10).encode("utf-8"), tags="dev"),
            Note(content=fake.text(10).encode("utf-8"), tags="dev"),
            Note(content=fake.text(10).encode("utf-8"), tags="test,dev"),
            Note(content=fake.text(10).encode("utf-8"), tags="test,dev"),
            Note(content=fake.text(10).encode("utf-8"), tags="dev,test"),
            Note(content=fake.text(10).encode("utf-8"), tags="dev,test"),
        ]

        db = NoteDatabase(Database)

        for note in notes:
            db.insert_note(note)

        matches = db.select_note_by_tags(tag_set_one)
        for match in matches:

            matched_tags = set(match.tags.strip().split(","))

            self.assertTrue(tag_set_one[0] in matched_tags)

        matches = db.select_note_by_tags(tag_set_two)
        for match in matches:

            matched_tags = set(match.tags.strip().split(","))

            self.assertTrue(str(tag_set_two[0]) in set(matched_tags))

        matches = db.select_note_by_tags(tag_set_three)
        for match in matches:

            matched_tags = set(match.tags.strip().split(","))

            self.assertTrue(set(tag_set_three) in set(matched_tags))

        matches = db.select_note_by_tags(tag_set_four)
        for match in matches:

            matched_tags = set(match.tags.strip().split(","))

            self.assertTrue(set(tag_set_four) in set(matched_tags))

        matches = db.select_note_by_tags([])

        self.assertFalse(matches)

        matches = db.select_note_by_tags(tag_set_five)

        self.assertFalse(matches)
