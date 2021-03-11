

class Table:
    pass


class Note:
    def __init__(self, note_id: int = None, content: bytes = None, date=None, active: bool = None) -> None:
        self.note_id = note_id
        self.content = content
        self.date = date
        self.active = active

    def __repr__(self) -> str:
        return str(self.note_id) + " " + str(self.content)

    @staticmethod
    def file_to_binary(filename):
        """
        Convert text file to binary blob
        """
        with open(filename, "rb") as f:
            data = f.read()

        return data.hex()

    @staticmethod
    def binary_to_string(b_string):
        """
        Convert binary to string
        """
        return bytes.fromhex(b_string).decode("utf-8")

    def get_content(self) -> dict:

        return self.content


class Tag:
    pass
