"""
menu.py


Build and execute query's

"""

from Note.database import NoteDatabase
from Note.display import NoteDisplay
from Note.request import NoteRequest


class Executor:
    """Base Class for Executors.

    Class function from pass arguments

    """

    def __init__(self, args: dict):
        """
        Args:
            args: dictionary of executor arguments.

            .. note::

               The key `func` must hold a executor. 
        """

        self.args = args

    def execute(self):
        """Handle Command

        Executes the default function within args.

        Raises:
            TypeError: "Executor Not Supported"
        """

        if not self.args.get("menu"):
            return

        try:
            self.args.get("func")(self.args).execute()
        except TypeError as e:
            if not self.args.get("func"):
                raise TypeError("Executor Not Supported or not defined") from e


class ListMenuExecutor(Executor):

    """List Executor

    The list executor handles the list command.
    """

    DEFAULT = None

    def __init__(self, args):
        super().__init__(args)
        """
        Args:
            args: dictionary of arguments.
                limit int: Limits displayed notes
        """

        self.limit = args.get("limit", self.DEFAULT)
        self.range = args.get("range", self.DEFAULT)
        self.tag = args.get("tag", self.DEFAULT)

    def execute(self):

        with NoteDatabase.get_database() as db:
            request = NoteRequest(
                limit=self.limit,
                tag=self.tag)
            notes = db.read(request)
            NoteDisplay(notes).show()
