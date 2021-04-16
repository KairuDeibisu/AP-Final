import unittest
from Note.cli.manage import get_message_from_editor
import os
import sys
import subprocess


class TestNoteManageCreate(unittest.TestCase):

    def test_get_note_message(self):

        message = get_message_from_editor("vim")

        if message:
            self.assertEqual(str, type(message))

        message = get_message_from_editor("nano")

        if message:
            self.assertEqual(str, type(message))

        self.assertRaises(
            NotImplementedError,
            get_message_from_editor,
            "fakeeditor")
