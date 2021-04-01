"""
display.py

Handle output, handles output of the application

"""

import abc
from typing import Iterable
from Note.table import Note, Tag


class Display(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def show(self):
        """ Display Object """

        pass


class NoteDisplay(Display):

    def __init__(self, items: Iterable[Note]) -> None:
        super().__init__()

        self.items = items

    def show(self):
        for item in self.items:
            if (tags := item.get_tags()) != None:
                tags = ", ".join(item.get_tags())
            print()
            print("ID ", item.get_id())
            print("Tags: ", tags)
            print("Date: ", item.get_date())
            print(f"\t{item.get_content_string()}")
