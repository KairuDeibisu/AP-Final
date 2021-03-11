import sys
from Note.database import get_database
from Note.table import Note


def main(argv) -> int:
    note = Note(content=Note.file_to_binary("test.txt"))

    with get_database() as database:

        for note in database.get_note_by_id(1):
            print(note)


if __name__ == "__main__":

    exit(main(sys.argv))
