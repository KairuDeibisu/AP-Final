from os import stat
from typing import Generator
from Note import DEFAULT_CONFIGURATION_PATH
from Note.table import Note
import mysql.connector
import json


NOTES_TABLE = """
CREATE TABLE IF NOT EXISTS note(
	note_id INT AUTO_INCREMENT PRIMARY KEY,
	content BLOB NOT NULL,
	date_created DATE NOT NULL DEFAULT (CURDATE()),
	active BOOL NOT NULL DEFAULT true
);
"""

TAGS_TABLE = """
CREATE TABLE IF NOT EXISTS tag(
	fk_note_id INT,
	name VARCHAR(255) NOT NULL,
	FOREIGN KEY (fk_note_id) REFERENCES note(note_id),
	PRIMARY KEY(fk_note_id, name)
);
"""

DATABASE_NAME = "notes"


class Database:

    """
    Base class for database.
    """

    def __init__(self, user, password, host, database=None) -> None:
        self.connect(user, password, host, database)
        self._cursor = self._db.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type != 0:
            self._db.close()
            return False

        return True

    def execute(self, query, args: tuple = None):
        self._cursor.execute(query, args)

    def commit(self):
        self._db.commit()

    def connect(self, user, password, host, database=None):
        self._db = mysql.connector.connect(
            user=user, passwd=password, host=host, database=database)

    def cursor(self):
        return self._cursor


class NoteDatabase(Database):

    ORDER_BY_DATE = "ORDER BY date_created"

    def insert_note(self, note) -> int:
        """
        Insert a note into the database
        """
        self.execute(
            f"INSERT INTO note (content) VALUES (%s)",
            (note.get_content(),))
        self.commit()
        return self.cursor().lastrowid

    def get_all_notes(self, order=None) -> list[Note]:
        """
        Return a list of all notes
        """
        query = "SELECT * FROM note"

        if order != None:
            query += " " + order

        query += ";"

        self.execute(query)
        return self._note_generator()

    def get_note_by_id(self, note_id: int) -> Note:
        """
        Return a note with given id 
        """
        self.execute("SELECT * FROM note WHERE note_id = %s;", (note_id,))
        return next(self._note_generator())

    def _note_generator(self) -> Generator:
        """
        Return a generator of notes from the current qurey
        """
        for note in self.cursor():
            yield self._convert_note(note)

    def _convert_note(self, note: tuple):
        """
        Convert note from sql qurey into python object
        """
        return Note(note[0], note[1], note[2], bool(note[3]))

    @staticmethod
    def _build_tables(database):
        """
        Create database tables 
        """
        database.execute(NOTES_TABLE)
        database.execute(TAGS_TABLE)

    @staticmethod
    def _initialize_database(database):
        """
        Sets up MySQL database
        """
        try:
            database.execute(
                f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} DEFAULT CHARACTER SET 'utf8';")
            database.commit()
        except mysql.connector.Error as err:
            print("Could not create database %s", err)
            exit(1)

        NoteDatabase.initialize_tables(database)

        return database

    @staticmethod
    def _initialize_tables(database):
        """
        Set up MYSQL tables
        """
        database.execute(f"USE {DATABASE_NAME};")
        NoteDatabase.build_tables(database)
        database.commit()

    @staticmethod
    def _database_configuration(path: str) -> dict:
        """
        Load configuration from file
        """
        with open(path, "r") as f:
            data = json.load(f)

        return data

    @staticmethod
    def get_database():
        """
        Get configured note database
        """
        auth = NoteDatabase._database_configuration(
            DEFAULT_CONFIGURATION_PATH)
        return NoteDatabase._initialize_database(NoteDatabase(auth["user"], auth["password"], auth["host"]))
