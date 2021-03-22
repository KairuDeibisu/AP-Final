
"""
table.py

Database table objects

"""

import datetime

from datetime import date, datetime


class Note:
    """
    Note class stores data about note
    """

    def __init__(self,
                 note_id: int = None,
                 content: bytes = None,
                 date: date = None,
                 active: bool = None,
                 file=None) -> None:
        self.note_id = note_id
        self.set_content(content)
        self.set_date(date)
        self.active = active

        if file != None:
            self.set_content_from_file(file)

    def __str__(self) -> str:
        return self.str()

    def __repr__(self) -> str:
        return str((self.note_id, self.content, self.date, self.active))

    def str(self):
        """
        Return object as a formated string
        """
        return f"\nID:{self.note_id} Created:{self.date}\n" \
            + ("-" * 30) + \
            f"\n{self.get_content_string()}\n" \
            + ("-" * 30)

    def set_content_from_file(self, path):
        with open(path, "r") as f:
            self.set_content(f.read())

    def get_id(self) -> int:
        return self.note_id

    def set_id(self, note_id: int):
        self.note_id = note_id

    def get_active(self):
        return self.active

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
        return self.date

    def set_date(self, date: datetime):

        if date == None:
            self.date = datetime.now().date()
            return

        self.date = date


class Tag:
    pass
