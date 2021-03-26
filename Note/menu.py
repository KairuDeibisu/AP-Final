from Note.database import NoteDatabase


ListMenu = None


class Executor:

    menus = [ListMenu]

    def __init__(self, args):
        self.args = args

    def execute(self):

        for menu in self.menus:
            if menu.MENU_NAME == self.args.get("menu"):
                self.menus(self.args).execute()


class ListMenu(Executor):

    MENU_NAME = "list"
    DEFAULT = None

    def __init__(self, args):
        super().__init__(args)

        self.limit = args.get("limit", self.DEFAULT)
        self.date = args.get("date", self.DEFAULT)
        self.tags_list = args.get("tags", self.DEFAULT)

    def execute(self):

        with NoteDatabase.get_database() as db:
            pass
