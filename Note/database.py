"""
Platform:
    Unix, Windows

Synopsis:
    Database Connection and Managment.
"""

import json
import abc
from typing import Any, Iterable, Tuple
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

    """Base class for database.

    Handles connection to the database.

    .. note::

       Overide to connect to a new relational database managament system.

    """

    def __init__(self,
                 user: str,
                 password: str,
                 host: str,
                 database: str = None) -> None:
        """Configure a database instance.

        Args:
            user: database username
            password: database password
            host: database ip

        Kwargs:
            database: select what database to use
                'USE note'

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

    def execute(self, query: str, args: Tuple = None, multi: bool = False):
        """Execute query to the database.

        Executes given query to the currently connected database instance.

        Args:
            query: A MYSQL query statment.

            args: Arguments for the current query.

            multi: Specify where query has more then one statment. Arguments should not be passed in this case.

            >>> execute("USE notes; SELECT * FROM note;", multi=True)


        """
        self.cursor().execute(query, args, multi=multi)

    def commit(self):
        """Commit Changes

        Commit changes to the current database instance.
        """
        self._db.commit()

    def cursor(self) -> cursor:
        """Get a database cursor

        Gets database cursor thats connected to the current database.

        Returns:
            A cursor object to the currently conected database instance. Holds the output of execute.
                >>> db.read(request)
                >>> for note in db.cursor(): print(note)

        """
        return self._cursor

    def _connect(self):
        """Connect to the database

        Connect to the current database management system.
        """
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
        """Configure Database

        Configure database from configuration file.

        Returns:
            A dict conntaning server configuration.
                {"host": "localhost","user": "root",
                 "password": "password1"}

            If keys not found the program will fail to connect to the database.

        Raises:
            FileNotFoundError: Configuration file not found
        """

        try:
            with open(path, "r") as f:
                return json.load(f)

        except FileNotFoundError as e:
            raise FileNotFoundError("Configuration file not found!") from None


class IDatabase(metaclass=abc.ABCMeta):

    """Database interface for database operations.

    Interface for current database. This allows for easy switching of database managment systems.

    .. note::

       Databases should inherit this interface.

    """

    @abc.abstractmethod
    def create(self, request: Request) -> int:
        """Create database entry.

        Send a create request to the currently connect database.

        Args:
            request: Request to make to the database. Object that translates user input to MYSQL statements.
        """
        pass

    @abc.abstractmethod
    def update(self, request: Request):
        """Update database entry.

        Send a update request to the currently connect database.

        Args:
            request: Request to make to the database. Object that translates user input to MYSQL statements.
        """
        pass

    @abc.abstractmethod
    def read(self, request: Request) -> Iterable[Any]:
        """Read from database.

        Send a read request to the currently connect database.

        Args:
            request: Request to make to the database. Object that translates user input to MYSQL statements.

        Returns:
            A iterable objects.
        """
        pass

    @abc.abstractmethod
    def delete(self, request: Request):
        """Delate database entry.

        Send a delete request to the currently connect database.

        Args:
            request: Request to make to the database. Object that translates user input to MYSQL statements.
        """
        pass

    @abc.abstractstaticmethod
    def get_database(self) -> Database:
        """Get Database

        Get configured database

        Returns:
            A configured database instance.
        """
        pass


class NoteDatabase(Database, IDatabase):

    """
    NoteDatabase handles the database operations
    """

    def read(self, request: Request) -> Iterable[any]:
        query, args = request.select_query()

        self.execute(query, args)

        if type((type_ := request.get_type())) == type(Note):
            return self._get_notes()

        raise NotImplementedError("{type_} Can't support return type!")

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

    def _get_notes(self) -> list:
        """Genearate notes from current query.

        Returns:
            A list of notes from the current qurey.
        """
        return list(map(self._convert_note, self.cursor()))

    def _convert_note(self, note: tuple) -> Note:
        """Convert note from sql query into python Note object.

        Returns:
            A note object.
        """

        return Note(note_id=note[0],
                    content=note[1],
                    date_=note[2],
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
