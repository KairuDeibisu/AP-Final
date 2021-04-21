

import re
import sqlalchemy

from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import VARCHAR
from Note.cli import CONFIGRATION
from Note.database.table import Note, Tag

from datetime import datetime
from abc import abstractmethod, abstractclassmethod, abstractproperty, abstractstaticmethod
from typing import Optional, List, Any
import abc

from sqlalchemy import MetaData, BLOB, Table, Column, engine, ForeignKeyConstraint, String, Boolean, Date, Integer, select, desc
from sqlalchemy import create_engine



class Database:

    db_path = "notes.db"
    metadata = MetaData()
    
    user_table = Table(
            "note",
            metadata,
            Column("id", Integer(), primary_key=True, autoincrement=True),
            Column("content", BLOB, nullable=False),
            Column("date", Date(), default=datetime.now()),
            Column("active", Boolean(), default=True, nullable=False),
    )

    tag_table = tag_table = Table(
            "tag",
            metadata,
            Column("fk_note_id", Integer(), ForeignKey(user_table.c.id), primary_key=True),
            Column("name", String(255), primary_key=True)
    )
    
    _instance = None

    def __init__(self):

        self._init_database()

    def _init_database(self):
        """
        Build the database tables.
        """

        self.engine = create_engine(f"sqlite:///{Database.db_path}")

        with self.engine.begin() as conn:
            Database.metadata.create_all(conn)

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

    def insert_note(self, note: dict) -> int:
        """
        Insert note into database.
        """
        
        insert_stmt = self.db.user_table.insert().values(
            {"content": note.get("content").encode("utf-8")}
        )

        select_stmt = select(
            [self.db.user_table.c.id], 
            order_by=desc(self.db.user_table.c.id))
        
        with self.db.engine.begin() as conn:
            conn.execute(insert_stmt)
            result = conn.execute(select_stmt)
            return result.fetchone()
            
        
