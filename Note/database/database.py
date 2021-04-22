

from re import match
import re
from Note.cli import CONFIGRATION
from Note.database.table import Note, Base

from datetime import datetime
from typing import Iterable, Optional, List, final

from sqlalchemy import create_engine, engine
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.engine.base import Engine


class Database:

    _db_path = "notes.db"

    _instance = None

    def __init__(self):

        self._engine = None
        self._Session = None

        self._init_database()

    def _init_database(self):
        """
        Build the database tables.
        """

        self.engine = self.db_path

        Base.metadata.create_all(self.engine)

    def __new__(cls, *args, **kwargs):
        """
        Implement database singleton
        """

        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, path):
        self._engine = create_engine(f"sqlite:///{path}")
        self.Session = self.engine

    @property
    def Session(self):
        return self._Session

    @Session.setter
    def Session(self, engine: Engine):
        self._Session = sessionmaker(bind=engine)

    @property
    def db_path(self):
        return self._db_path

    @db_path.setter
    def db_path(self, path):

        self._db_path = path

        self._init_database()


class NoteDatabase:

    def __init__(self, database: Database):

        self.db = database()
        self._last_row_id = None

    def select_note(self, id_: int) -> Note:
        """
        Select notes from the database.
        """

        session = self.db.Session()

        match = session.query(Note).filter(Note.id_ == id_).first()

        return match

    def delete_note(self, id_: int) -> None:
        """
        Drop note from the database.
        """

        session = self.db.Session()

        match = session.query(Note).filter(Note.id_ == id_).first()

        session.delete(match)

        session.commit()

    def remove_note(self, id_: int) -> None:
        """
        Deactivate note from database.
        """

        session = self.db.Session()

        match = session.query(Note).filter(Note.id_ == id_).first()

        match.active = False

        session.commit()

    def insert_note(self, note: dict):
        """
        Insert note into the database.
        """

        session = self.db.Session()

        session.add(note)

        session.commit()

        self.last_row_id = session

    def select_note_by_tags(self, tags: List[str]):
        """
        Select note by tags
        """

        session = self.db.Session()

        matches = session.query(Note).all()

        final_matches = []

        for match in matches:

            if match.tags == None:
                continue

            matched_tags = set(match.tags.strip().split(","))

            if len(set(tags)) == 1 and tags[0] in set(matched_tags):
                final_matches.append(match)

            elif set(tags) in set(matched_tags):
                final_matches.append(match)

        return final_matches

    def _set_last_row_id(self):

        session = self.db.Session()

        match = session.query(Note).first()
        self._last_row_id = match.records.order_by(
            None).order_by(match.id_.desc()).first()

    @property
    def last_row_id(self):
        return self._last_row_id

    @last_row_id.setter
    def last_row_id(self, session):
        match = session.query(Note).order_by(
            None).order_by(Note.id_.desc()).first()
        self._last_row_id = match.id_
