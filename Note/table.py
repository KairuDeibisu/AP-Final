
"""
table.py

Database table objects

"""

from datetime import date


class Note:
    """
    Note class stores data about note
    """

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
    def file_to_binary(filename: str) -> bytes:
        """
        Convert text file to binary data

        :returns: contents

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
        except UnicodeDecodeError as err:
            raise Exception(
                f"Database Might be corrupt: {err}") from None
        except ValueError as err:
            raise Exception(f"not in hex format: {err}") from None

    def get_id(self) -> int:
        return self.note_id

    def set_id(self, table_id):
        self.note_id = table_id

    def get_active(self):
        return self.active

    def set_active(self, active):
        self.active = int(active)

    def set_content(self, content):
        self.content = content

    def get_content(self) -> str:

        return self.content

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date


class Tag:
    pass
