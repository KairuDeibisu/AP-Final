
"""
table.py

Database table objects

"""

from datetime import date

class Note:
    def __init__(self,
                 note_id: int = None,
                 content: bytes = None,
                 date: date = None,
                 active: bool = None) -> None:
        self.note_id = note_id
        self.content = content
        self.date = date
        self.active = active

    def __str__(self) -> str:

        return f"\nID:{self.note_id} Created:{self.date}\n" \
            + ("-" * 30) + \
            f"\n{Note.binary_to_string(self.content)}\n" \
            + ("-" * 30)

    def __repr__(self) -> str:
        return str((self.note_id, self.content, self.date, self.active))

    @staticmethod
    def file_to_binary(filename):
        """
        Convert text file to binary blob
        """
        with open(filename, "rb") as f:
            data = f.read()

        return data

    @staticmethod
    def binary_to_string(b_string: bytes):
        """
        Convert binary to string
        """
        try:
            return bytes.fromhex(b_string.decode()).decode('utf-8')
        except UnicodeDecodeError:
            print("Error: Database Might be corrupt")
            exit(1)

    def get_content(self) -> dict:

        return self.content


class Tag:
    pass
