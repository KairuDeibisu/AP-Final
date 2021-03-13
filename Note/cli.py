"""
cli.py

handle user input, is the entry point to the application 
"""
import sys
from Note.database import NoteDatabase as db
from Note.table import Note


def main(argv) -> int:
    note = Note(content=Note.file_to_binary("test.txt"))

    with db.get_database() as database:
        for note in database.get_all_notes(order=db.ORDER_BY_DATE):
            print(note)


if __name__ == "__main__":

    exit(main(sys.argv))
