

from Note.cli.__main__ import app
from Note.database.database import NoteDatabase, Database
from Note.database.table import Note

from typing import List
import re


from unittest import runner
import unittest

from typer.testing import CliRunner
from faker import Faker


class TestCLI(unittest.TestCase):

    runner = CliRunner()
    regex_get_id_line_pattern = r"(ID:\s+(\d+))"

    db = NoteDatabase(Database)

    def test_manage(self):
        """
        Test manage subcommands
        """
        result = self.runner.invoke(app, ["manage"])
        self.assertEqual(result.exit_code, 0)

    def test_manage_create(self):
        """
        Test create command
        """

        result = self.runner.invoke(app, ["manage", "add", "-m"])
        self.assertGreaterEqual(result.exit_code, 1)

        result = self.runner.invoke(
            app, ["manage", "add", "-m", "Hello, World"])
        self.assertIn("Hello, World", result.stdout)

        result = self.runner.invoke(
            app, ["manage", "add", "-m", "Hello, World", "-t", "test"])
        id_ = self.get_id_from_console(result.stdout)
        notes_with_tag_test = [tag[0] for tag in self.db.select_tag_id("test")]
        self.assertIn(id_, notes_with_tag_test)

        result = self.runner.invoke(
            app, ["manage", "add", "-m", "Hello, World", "-t", "test", "-t", "dev"])
        id_ = self.get_id_from_console(result.stdout)
        notes_with_tag_test = [tag[0] for tag in self.db.select_tag_id("test")]
        notes_with_tag_dev = [tag[0] for tag in self.db.select_tag_id("dev")]
        self.assertIn(id_, notes_with_tag_test)
        self.assertIn(id_, notes_with_tag_dev)

    def test_manage_remove(self):
        """
        Test remove command
        """

        result = self.runner.invoke(app, ["manage", "remove"])
        self.assertGreaterEqual(result.exit_code, 1)

        note = Note(content="Hello, World".encode("utf-8"))
        self.db.insert_note(note)
        id_ = self.db.last_row_id
        result = self.runner.invoke(app, ["manage", "remove", str(id_)])
        self.assertEqual(result.exit_code, 0)
        result = self.db.select_note_by_id(id_)
        self.assertFalse(result.active)

        result = self.runner.invoke(
            app, ["manage", "remove", str(id_), "--delete"])
        self.assertEqual(result.exit_code, 0)
        result = self.db.select_note_by_id(id_)
        self.assertIsNone(result)

    def test_manage_recover(self):
        """
        Test recover command.
        """

        note = Note(content="Hello, World".encode("utf-8"), active=False)
        self.db.insert_note(note)
        id_ = self.db.last_row_id

        result = self.runner.invoke(app, ["manage", "recover"])
        self.assertGreaterEqual(result.exit_code, 1)

        result = self.runner.invoke(app, ["manage", "recover", str(id_)])
        self.assertEqual(result.exit_code, 0)

        result = self.db.select_note_by_id(id_)
        self.assertTrue(note.id_)

    def test_search(self):
        """
        Test search subcommands
        """
        result = self.runner.invoke(app, ["search"])
        self.assertEqual(result.exit_code, 0)

    def test_search_id(self):
        """
        Test id command
        """

        result = self.runner.invoke(app, ["search", "id"])
        self.assertGreaterEqual(result.exit_code, 1)

        result = self.runner.invoke(app, ["search", "id", "j"])
        self.assertGreaterEqual(result.exit_code, 1)

        note = Note(content="Hello, World".encode("utf-8"))
        self.db.insert_note(note)
        id_ = self.db.last_row_id

        result = self.runner.invoke(app, ["search", "id", str(id_)])
        self.assertEqual(self.get_id_from_console(result.stdout), id_)

        note = Note(content="Hello, World".encode("utf-8"), active=False)
        self.db.insert_note(note)
        id_ = self.db.last_row_id

        result = self.runner.invoke(app, ["search", "id", str(id_)])
        self.assertEqual(self.get_id_from_console(result.stdout), id_)

    def test_search_list(self):
        """
        Teat list command
        """
        result = self.runner.invoke(app, ["search", "list"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["search", "list"])
        self.assertEqual(result.exit_code, 0)
        result_id_list = self.get_all_ids_from_console(result.stdout)
        self.assertLessEqual(len(result_id_list), 5)

        result = self.runner.invoke(app, ["search", "list", "-h"])
        self.assertEqual(result.exit_code, 0)
        result_id_list = self.get_all_ids_from_console(result.stdout)
        self.assertLessEqual(len(result_id_list), 5)

        for id_ in result_id_list:
            note = self.db.select_note_by_id(id_)
            self.assertFalse(note.active)

        result = self.runner.invoke(app, ["search", "list", "--limit", "5"])
        self.assertEqual(result.exit_code, 0)
        result_id_list = self.get_all_ids_from_console(result.stdout)
        self.assertLessEqual(len(result_id_list), 5)

        result = self.runner.invoke(app, ["search", "list", "--limit", "100"])
        self.assertEqual(result.exit_code, 0)
        result_id_list = self.get_all_ids_from_console(result.stdout)
        self.assertLessEqual(len(result_id_list), 100)

        result = self.runner.invoke(app, ["search", "list", "--limit", "foo"])
        self.assertGreaterEqual(result.exit_code, 1)

    def test_search_tag(self):
        """
        Test tag command
        """

        # --- Test data --- #
        note = Note(content="Hello, World".encode("utf-8"))
        self.db.insert_note(note)
        id_ = self.db.last_row_id
        self.db.insert_tag(id_=id_, tags=["test"])

        note = Note(content="This is a hidden note!".encode(
            "utf-8"), active=False)
        self.db.insert_note(note)
        id_ = self.db.last_row_id
        self.db.insert_tag(id_=id_, tags=["test"])

        note = Note(content="Hello, World".encode("utf-8"))
        self.db.insert_note(note)
        id_ = self.db.last_row_id
        self.db.insert_tag(id_=id_, tags=["dev"])

        note = Note(content="Hello, World".encode("utf-8"))
        self.db.insert_note(note)
        id_ = self.db.last_row_id
        self.db.insert_tag(id_=id_, tags=["dev", "test"])

        # --- Starting Tests --- #
        result = self.runner.invoke(app, ["search", "tag", "-t", "test", "-h"])
        result_id_list = self.get_all_ids_from_console(result.stdout)
        test_tag_id_list = [
            tag.fk_note_id for tag in self.db.select_tag("test")]

        for id_ in result_id_list:
            self.assertIn(int(id_), test_tag_id_list)

        result = self.runner.invoke(app, ["search", "tag", "-t", "test"])
        result_id_list = self.get_all_ids_from_console(result.stdout)
        test_tag_id_list = [
            tag.fk_note_id for tag in self.db.select_tag("test")]

        for id_ in result_id_list:
            self.assertIn(int(id_), test_tag_id_list)

        result = self.runner.invoke(app, ["search", "tag", "-t", "dev"])
        result_id_list = self.get_all_ids_from_console(result.stdout)
        dev_tag_id_list = [tag.fk_note_id for tag in self.db.select_tag("dev")]

        for id_ in result_id_list:
            self.assertIn(int(id_), dev_tag_id_list)

        result = self.runner.invoke(
            app, ["search", "tag", "-t", "test", "-t", "dev"])
        result_id_list = self.get_all_ids_from_console(result.stdout)
        dev_test_tag_id_list = [
            note.id_ for note in self.db.select_note_by_tags(["test", "dev"])]

        for id_ in result_id_list:
            self.assertIn(int(id_), dev_test_tag_id_list)

    def get_all_ids_from_console(self, result: str) -> List[int]:
        pattern = re.compile(self.regex_get_id_line_pattern)
        outputs = pattern.findall(result)
        id_list = [result[1] for result in outputs]
        return id_list

    def get_id_from_console(self, result: str) -> int:
        pattern = re.compile(self.regex_get_id_line_pattern)
        id_ = pattern.search(result).group(2)
        return int(id_)
