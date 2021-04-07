
"""
table.py

Database table objects

"""

from datetime import date, datetime
from typing import List


class Tag:
    pass


class Note:
    """dataclass repersenting a note."""

    def __init__(self,
                 note_id: int = None,
                 content: bytes = None,
                 date_: date = None,
                 active: bool = None,
                 file=None) -> None:
        self.note_id = note_id
        self.set_content(content)
        self.set_date(date_)
        self.active = active
        self.tags = None

        if file != None:
            self.set_content_from_file(file)

    def __str__(self) -> str:
        return self.str()

    def __repr__(self) -> str:
        return str((self.note_id, self.content, self.date_, self.active))

    def __eq__(self, o: object) -> bool:
        if isinstance(o, type(self)):
            return self.get_id() == o.get_id()

        return False

    def str(self):
        """
        Return object as a formated string
        """
        return f"\nID:{self.note_id} Created:{self.date_}\n" \
            + ("-" * 30) + \
            f"\n{self.get_content_string()}\n" \


    def set_content_from_file(self, path):
        with open(path, "r") as f:
            self.set_content(f.read())

    def get_id(self) -> int:
        return self.note_id

    def set_id(self, note_id: int):
        self.note_id = note_id

    def get_active(self):
        return self.active

    def set_tags(self, tags: List[Tag]):
        self.tags = tags

    def get_tags(self) -> List[Tag]:
        return self.tags

    def set_active(self, active: int):
        self.active = int(active)

    def set_content(self, content: bytes):

        if content == None:
            self.content = content
            return

        if isinstance(content, bytes):
            self.content = content
            return

        self.content = content.encode("utf-8")

    def get_content(self) -> bytes:

        return self.content

    def get_content_string(self) -> str:
        return self.content.decode("utf-8")

    def get_date(self):
        return self.date_

    def set_date(self, date_: datetime):

        if date_ == None:
            self.date_ = datetime.now().date()
            return

        self.date_ = date_