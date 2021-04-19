

from Note.cli import CONFIGRATION
from Note.database.table import Note, Tag

from datetime import datetime
from abc import abstractmethod, abstractclassmethod, abstractproperty, abstractstaticmethod
from typing import Optional, List
import abc

from sqlalchemy import MetaData, BLOB, INTEGER, DATE, BOOLEAN, Table, Column, engine
from sqlalchemy import create_engine



class Database:

    _instance = None


    def __init__(self):
        
        self._init_database

    
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

    def __new__(cls, *args,**kwargs):
        """
        Implement database singleton
        """

        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)

        return cls._instance

class NoteDatabase:

    def __init__(self, database:Database):
        self.db = database()

    
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
