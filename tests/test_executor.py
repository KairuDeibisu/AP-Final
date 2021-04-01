
import unittest
from Note.executor import Executor, ListMenuExecutor


class TestExecutor(unittest.TestCase):

    def test_supported_executor_error(self):
        """
        Raise error if exector is not supported
        """

        self.assertRaises(TypeError, Executor({"func": None}))
        self.assertRaises(TypeError, Executor({"func": ""}))


class TestListMenuExecutor(unittest.TestCase):

    menu = ListMenuExecutor({"limit": 5})

    def test_is_subclass(self):
        """
        Menu is subclass of Executor
        """
        self.assertTrue(issubclass(ListMenuExecutor, Executor))

    def test_search_tag(self):
        """
        Menu returns results with tag
        """
        pass
