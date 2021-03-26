
import unittest
from Note.menu import Executor, ListMenu


class TestListMenu(unittest.TestCase):

    def test_menu_name(self):
        """
        Menu has a name
        """

        self.assertEqual(ListMenu.MENU_NAME, ListMenu.MENU_NAME)

    def test_is_subclass(self):
        """
        Menu is subclass of Executor
        """
        self.assertTrue(issubclass(ListMenu, Executor))

    def test_search_limit(self):
        """
        Menu returns results limited
        """
        pass

    def test_search_date(self):
        """
        Menu returns results by date
        """
        pass

    def test_search_tag(self):
        """
        Menu returns results with tag
        """
        pass
