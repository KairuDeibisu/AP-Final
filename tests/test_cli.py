
from unittest import runner
from Note.cli.__main__ import app

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

        # FIXME: Handle error if number is passed in insted of string.
        # result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t", "1"])
        # self.assertGreaterEqual(result.exit_code, 1)

        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t", "test"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t", "test", "-t", "dev"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t", "test", "-t", "dev-test"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["manage", "create", "-m", "Hello, World", "-t", "test", "-t", "dev test"])
        self.assertEqual(result.exit_code, 0)