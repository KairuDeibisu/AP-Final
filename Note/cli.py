import sys
from Note.database import NoteDatabase, get_database
from Note.table import Note


def main(argv) -> int:
    note = Note(content=Note.file_to_binary("test.txt"))

    with get_database() as database:
        for note in database.get_all_notes(order=NoteDatabase.ORDER_BY_DATE):
            print(note)


if __name__ == "__main__":

    exit(main(sys.argv))
