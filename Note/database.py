"""
database.py

Database objects

"""

import json
import abc
from re import MULTILINE
from typing import Generator, Iterable
from Note import DEFAULT_CONFIGURATION_PATH
from Note.table import Note
from Note.request import Request
import mysql.connector
from mysql.connector import cursor


NoteDatabase = None

NOTES_TABLE = """
CREATE TABLE IF NOT EXISTS note(
	note_id INT AUTO_INCREMENT PRIMARY KEY,
	content BLOB NOT NULL,
	date_created DATE NOT NULL DEFAULT (CURDATE()),
	active BOOL NOT NULL DEFAULT true
)  ENGINE=INNODB;
"""

TAGS_TABLE = """
CREATE TABLE IF NOT EXISTS tag(
	fk_note_id INT,
	name VARCHAR(255) NOT NULL,
	FOREIGN KEY (fk_note_id) REFERENCES note(note_id),
	PRIMARY KEY(fk_note_id, name)
)  ENGINE=INNODB;
"""

DATABASE_NAME = "notes"


class Database:

    """
    Base class for database.
    """

    def __init__(self,
                 user: str,
                 password: str,
                 host: str,
                 database: str = None) -> None:
        """
        :param user: database username
        :param password: database password
        :param host: database ip
        :param database: select what database to use
        """
        self._user = user
        self._password = password
        self._host = host
        self._database = database

        self._connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type != 0:
            self._db.close()
            return False

        self._db.close()
        return True

    def execute(self, query, args: tuple = None, multi=False):
        """
        Execute query to the database.

        :param query: MYSQL query
        :param args: query arguments

        """
        self.cursor().execute(query, args, multi=multi)

    def commit(self):
        """
        Commit changes to the database
        """
        self._db.commit()

    def cursor(self) -> cursor:
        """
        :returns: a cursor object that's conected to the database. Holds the output of execute. 
        """
        return self._cursor

    def _connect(self):
        self._db = mysql.connector.connect(
            user=self._user,
            passwd=self._password,
            host=self._host,
            database=self._database)

        del self._password

        self._db.autocommit = False
        self._cursor = self._db.cursor(buffered=True)

    @staticmethod
    def _database_configuration(path: str) -> dict:
        """
        Load configuration from file
        """

        with open(path, "r") as f:
            data = json.load(f)

        return data


class IDatabase(metaclass=abc.ABCMeta):

    """
    Database interface for database operations.
    """

    @abc.abstractmethod
    def create(self, request: Request) -> int:
        """
        Create a note object in the database.

        :param request: request to make to the database
        :returns: note_id
        """
        pass

    @abc.abstractmethod
    def update(self, request: Request):
        """
        Update a note entry in the database.

        :param request: request to make to the database
        """
        pass

    @abc.abstractmethod
    def read(self, request: Request) -> Iterable[Note]:
        """

        Read note entrys from database.

        :param request: request to make to the database
        :returns: a note object from the table
        """
        pass

    @abc.abstractmethod
    def delete(self, request: Request):
        """
        Delete note from database.

        :param request: request to make to the database
        """
        pass

    @abc.abstractstaticmethod
    def get_database(self) -> Database:
        """
        Get configured note database

        :returns: a database
        """
        pass


class NoteDatabase(Database, IDatabase):

    """
    NoteDatabase handles the database operations
    """

    def read(self, request: Request) -> Note:
        query, args = request.select_query()

        self.execute(query, args)

        return self._note_generator()

    def create(self, request: Request) -> int:

        query, args = request.create_query()

        self.execute(query, args)
        self.commit()

        return self.cursor().lastrowid

    def update(self, request: Request):
        query, args = request.update_query()

        self.execute(query, args)
        self.commit()

    def delete(self, request: Request):

        query, args = request.delete_query()

        tags_delete, note_delete = query.split(";", 1)
        self.execute(tags_delete + ";", (args[0],))
        self.execute(note_delete, (args[1],))

        self.commit()

    def _note_generator(self) -> Generator:
        """
        Genearate notes from current query

        :returns: a generator of notes from the current qurey
        """
        for note in self.cursor():
            yield self._convert_note(note)

    def _convert_note(self, note: tuple) -> Note:
        """
        Convert note from sql query into python Note object

        :returns: a note object
        """

        return Note(note_id=note[0],
                    content=note[1],
                    date=note[2],
                    active=note[3])

    @staticmethod
    def _build_tables(database: Database):
        """
        Create database tables

        :param database: connected database
        """
        database.execute(NOTES_TABLE)
        database.execute(TAGS_TABLE)

    @staticmethod
    def _initialize_database(database: Database):
        """
        Sets up MySQL database

        :param database: connected database
        """

        query = f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} DEFAULT CHARACTER SET 'utf8';"

        try:
            database.execute(query)
            database.commit()
        except mysql.connector.Error as err:
            raise Exception(f"Could not create database: {err}") from None

        NoteDatabase._initialize_tables(database)

        return database

    @staticmethod
    def _initialize_tables(database: Database):
        """
        Set up MYSQL tables

        :param database: connected database
        """

        query = f"USE {DATABASE_NAME};"

        database.execute(query)
        NoteDatabase._build_tables(database)

        database.commit()

    @staticmethod
    def get_database() -> NoteDatabase:

        auth = Database._database_configuration(DEFAULT_CONFIGURATION_PATH)
        db = NoteDatabase(auth["user"], auth["password"], auth["host"])

        return NoteDatabase._initialize_database(db)
