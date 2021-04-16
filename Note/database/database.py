

from Note.cli import CONFIGRATION
from Note.database.table import Note, Tag

from datetime import datetime
from abc import abstractmethod, abstractclassmethod, abstractproperty, abstractstaticmethod
from typing import Optional, List
import abc

from sqlalchemy import MetaData, BLOB, INTEGER, DATE, BOOLEAN, Table, Column, engine
from sqlalchemy import create_engine


class INoteDatabase(metaclass=abc.ABCMeta):
    """
    Database operations specific to the Notes database.
    """

    def __init__(
            self,
            password: str = None):
        """
        Connect to database.
        """

        self.password = password if password else CONFIGRATION.get("password")

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
        Drop note from the database.
        """
        pass

    @abstractmethod
    def select_note(self) -> List[Note]:
        """
        Select notes from the database.
        """
        pass

    @abstractmethod
    def _init_database(self):
        """
        Create notes database.
        """
        pass


class NoteDatabase(INoteDatabase):

    def __init__(self, password: str = None):
        super().__init__(password=password)

        self._init_database()

    def select_note(self) -> List[Note]:
        """
        Select notes from database.
        """
        pass

    def delete_note(self) -> None:
        """
        Drop note from database.
        """
        pass

    def remove_note(self) -> None:
        """
        Deactivate note from database. 
        """
        pass

    def insert_note(self) -> int:
        """
        Insert note into database.
        """
        pass

    def _init_database(self):

        metadata = MetaData()

        self.user_table = Table(
            "note",
            metadata,
            Column("id", INTEGER, primary_key=True, autoincrement=True),
            Column("content", BLOB, nullable=False),
            Column("date", DATE, default=datetime.now()),
            Column("active", BOOLEAN, default=True, nullable=False)
        )

        engine = create_engine("sqlite:///notes.db")

        with engine.begin() as conn:
            metadata.create_all(conn)
