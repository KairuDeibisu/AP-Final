
import unittest
from Note.menu import Executor, ListMenu
from Note.database import NoteDatabase


class TestListMenu(unittest.TestCase):

    menu = ListMenu({"limit": 5})

    def test_is_subclass(self):
        """
        Menu is subclass of Executor
        """
        self.assertTrue(issubclass(ListMenu, Executor))

    def test_search_tag(self):
        """
        Menu returns results with tag
        """
        pass
