

from Note.database.table import Note, Base, Tag
from Note.utils.algorithm import divide_and_conquer

from typing import Iterable, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine


class Database:

    """
    Database object that handles connection to a database.    
    """

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

    """
    Application database interface.
    """

    def __init__(self, database: Database):
        """
        Constructor

        Args:
            database: A connected database object.

        """

        self.db = database()
        self._last_row_id = None

    def select_note_by_id(self, id_: int) -> Note:
        """
        Select notes from the database.

        Args:
            id_: The id of the note to select.

        Returns:
            A note object with the given id_.
        """

        session = self.db.Session()

        matched = session.query(Note).filter(Note.id_ == id_).first()

        return matched

    def select_note(self, limit: int = None, active=True) -> List[Note]:
        """
        Select all notes from database.

        Args:
            limit: The max number of notes returned.
            active: The status of the notes returned. (Hidden/Unhidden)

        Returns:
            A list of note objects.
        """

        session = session = self.db.Session()

        matched = session.query(Note).filter(Note.active == active).order_by(
            Note.id_.desc()).limit(limit).all()

        return matched

    def delete_note(self, id_: int) -> None:
        """
        Drop note from the database.

        Args:
            id_: The id of the note to delete. This is permanent.

        """

        session = self.db.Session()

        matched = session.query(Note).filter(Note.id_ == id_).first()

        session.delete(matched)

        session.commit()

    def set_note_active_value(self, id_: int, value: bool) -> None:
        """
        Activate and Deactivate note from database.

        Args:
            id_: The id of the note to assign value.
            value: The value to assign to id.

        """

        session = self.db.Session()

        matched = session.query(Note).filter(Note.id_ == id_).first()

        matched.active = value

        session.commit()

    def insert_note(self, note: Note) -> None:
        """
        Insert note into the database.

        Args:
            note: The note object to insert into the database.

        .. Note:
            The properly last_row_id is set with the id of the inserted note. 

        """

        session = self.db.Session()

        session.add(note)

        session.commit()

        self.last_row_id = session

    def select_note_by_tags(self, tags: List[str], limit=None, active=True) -> Iterable[Note]:
        """
        Get a list of notes that match the given tags.

        Args:
            tags: The tags that all returned notes have.
            limit: The max number of notes returned. Applied after filtering.
            active: The status of the notes returned. (Hidden/Unhidden)
        Returns:
            A iterable of note objects where each note matches all given tags.
        """

        session = self.db.Session()

        tag_matrix = []
        list_to_match = []

        for tag in tags:
            matched_id_list = [match[0]
                               for match in list(self.select_tag_id(tag))]
            tag_matrix.append(matched_id_list)
            list_to_match += matched_id_list

        list_to_match = set(list_to_match)

        matches = [
            id_ for id_ in list_to_match if self._common_element_in_lists(tag_matrix, id_)]

        matched = session.query(Note).filter(Note.id_.in_(
            matches), Note.active == active).limit(limit).all()

        return matched

    def insert_tag(self, id_: int, tags: List[str]) -> None:
        """
        Insert tag into the database

        Args:
            tags: The list of tags to insert into the database.
        """

        tags_to_insert = [Tag(fk_note_id=id_, name=tag) for tag in tags]

        session = self.db.Session()

        session.add_all(tags_to_insert)

        session.commit()

    def select_tag(self, tag: str) -> List[Tag]:
        """
        Get a list of tags that match the given tag.

        Args:
            tag: The tag selected tag.

        Returns:
            A list of tag objects.
        """

        session = self.db.Session()

        matched = session.query(Tag).filter(
            Tag.name == tag).order_by(Tag.fk_note_id.asc()).all()

        return matched

    def select_tag_id(self, tag: str) -> List[int]:
        """
        Get a list of note IDs that match the given tag.

        Args:
            tag: The select tag.

        Returns:
            A list of note object ID_'s that match the given tag.
        """

        session = self.db.Session()

        matched = session.query(Tag.fk_note_id).filter(
            Tag.name == tag).order_by(Tag.fk_note_id.asc()).all()

        return matched

    def _set_last_row_id(self):
        """
        Set the last row id.
        """

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

    @staticmethod
    def _common_element_in_lists(matrix: List[List[int]], key: int) -> bool:
        """
        Checks if the given element is a common element in all given lists.

        Args:
            matrix: A list that contains sorted lists, of note integers.

        >>> NoteDatabase._common_element_in_lists([[2,3,4,5],[1,3,4,5],[1,2,4,5]], 1)
        False
        >>> NoteDatabase._common_element_in_lists([[2,3,4,5],[1,3,4,5],[1,2,4,5]], 2)
        False
        >>> NoteDatabase._common_element_in_lists([[2,3,4,5],[1,3,4,5],[1,2,4,5]], 4)
        True
        >>> NoteDatabase._common_element_in_lists([[2,3,4,5],[1,3,4,5],[1,2,4,5]], 5)
        True

        """

        for list_ in matrix:
            if not divide_and_conquer(list_, key):
                return False

        return True
