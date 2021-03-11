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

    def __init__(self, user, passwd, host, database=None) -> None:

        self._db = mysql.connector.connect(
            user=user, passwd=passwd, host=host, database=database)

        self._cursor = self._db.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._db.close()
        return True

    def commit(self):
        self._db.commit()


class NoteDatabase(Database):

    def insert_note(self, note) -> int:
        """
        Insert a note into the database
        """
        content = note.get_content()

        self._cursor.execute(
            f"INSERT INTO note (content) VALUES ('{content}')", )
        self.commit()
        return self._cursor.lastrowid

    def get_notes(self) -> list:
        """
        Return a list of all notes
        """
        self._cursor.execute("SELECT * FROM note")
        return self._note_generator()

    def get_note_by_id(self, note_id) -> list:
        """
        Return a note with given id 
        """
        self._cursor.execute(f"SELECT * FROM note WHERE note_id = {note_id}")
        return self._note_generator()

    def _note_generator(self) -> Generator:
        """
        Return a generator of notes from the current qurey
        """
        for note in self._cursor:
            yield self._convert_note(note)

    def _convert_note(self, note: tuple):
        """
        Convert note from sql qurey into python object
        """
        return Note(note[0], note[1], note[2], note[3])

    @staticmethod
    def build_tables(database):
        """
        Create database tables 
        """
        database._cursor.execute(NOTES_TABLE)
        database._cursor.execute(TAGS_TABLE)
        database.commit()

    @staticmethod
    def initialize_database(database):
        """
        Sets up MySQL database and return it
        """
        try:
            database._cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} DEFAULT CHARACTER SET 'utf8';")
        except mysql.connector.Error as err:
            print("Could not create database %s", err)
            exit(1)
        database._cursor.execute(f"USE {DATABASE_NAME};")
        database.commit
        NoteDatabase.build_tables(database)
        return database

    @staticmethod
    def load_database_configuration(path) -> dict:
        """
        Load configuration
        """
        with open(path, "r") as f:
            data = json.load(f)

        return data


def get_database():
    """
    Get configured note database
    """
    auth = NoteDatabase.load_database_configuration(
        DEFAULT_CONFIGURATION_PATH)
    return NoteDatabase.initialize_database(NoteDatabase(auth["user"], auth["password"], auth["host"]))
