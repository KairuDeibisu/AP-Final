
from Note.cli import CONFIGRATION
from Note.database.table import Note, Tag

from abc import abstractmethod, abstractclassmethod, abstractproperty, abstractstaticmethod
from typing import Optional, List
import abc


class INoteDatabase(metaclass=abc.metaclass):
    """
    Database operations specific to the Notes database.
    """

    def __init__(
            self,
            password: str = None):
        """
        Connect to database.
        """

        self.password = password if password else CONFIGRATION["password"]

    @abstractmethod
    def insert_note(self) -> int:
        """
        Insert note into database.
        """
        pass

    @abstractmethod
    def remove_note(self) -> None:
        """
        Deactivate note from database. 
        """
        pass

    @abstractmethod
    def delete_note(self) -> None:
        """
        Drop note from database.
        """
        pass

    @abstractmethod
    def select_note(self) -> List[Note]:
        """
        Select notes from database.
        """
        pass
