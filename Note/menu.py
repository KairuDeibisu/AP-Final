"""
menu.py


Build and execute query's

"""

from Note.database import NoteDatabase
from Note.display import NoteDisplay


class Executor:

    def __init__(self, args):
        self.args = args

    def execute(self):

        for menu in menus:

            if self.args.get("menu") == None:
                return

            if menu.MENU_NAME == self.args.get("menu"):
                menu(self.args).execute()


class ListMenu(Executor):

    MENU_NAME = "list"
    DEFAULT = None

    def __init__(self, args):
        super().__init__(args)

        self.limit = args.get("limit", self.DEFAULT)
        self.tags_list = args.get("tags", self.DEFAULT)

    def execute(self):

        with NoteDatabase.get_database() as db:
            notes = db.read_all_notes(limit=self.limit)
            NoteDisplay(notes).show()


menus = [ListMenu]
