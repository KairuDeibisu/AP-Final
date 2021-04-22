
from unittest import runner
from Note.cli.__main__ import app
from Note.database.database import NoteDatabase, Database
from Note.database.table import Note


import unittest

from typer.testing import CliRunner


class TestCLI(unittest.TestCase):

    runner = CliRunner()

    def test_manage(self):
        result = self.runner.invoke(app, ["manage"])
        self.assertEqual(result.exit_code, 0)

    def test_manage_create(self):
        
        result = self.runner.invoke(app, ["manage", "create", "-m"])
        self.assertGreaterEqual(result.exit_code, 1)

        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t"])
        self.assertGreaterEqual(result.exit_code, 1)


        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t", "test"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t", "test", "-t", "dev"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t", "test", "-t", "dev-test"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t", "test", "-t", "dev test"])
        self.assertEqual(result.exit_code, 0)
    
    def test_search(self):
        result = self.runner.invoke(app, ["search"])
        self.assertEqual(result.exit_code, 0)
    

    def test_search_id(self):
        
        db = NoteDatabase(Database)

        result = self.runner.invoke(app, ["search", "id", "j"])
        self.assertGreaterEqual(result.exit_code, 1)
    
    def test_search_list(self):
        result = self.runner.invoke(app, ["search", "list"])
        self.assertEqual(result.exit_code, 0)
        
        result = self.runner.invoke(app, ["search", "list", "--limit", "5"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["search", "list", "--limit", "foo"])
        self.assertGreaterEqual(result.exit_code, 1)