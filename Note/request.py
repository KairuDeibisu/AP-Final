

import abc
import re
from typing import List, Tuple


class Request(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def select_query(self) -> Tuple[str, Tuple]:
        """
        Get constructed query

        :return: a query and it's arguments
        """
        pass

    @abc.abstractmethod
    def create_query(self) -> int:
        """
        Create Note
        :return: note id
        """
        pass

    @abc.abstractmethod
    def update_query(self) -> None:
        """
        Updated Note
        """
        pass

    @abc.abstractmethod
    def delete_query(self) -> None:
        """
        Delete Note
        """
        pass


class NoteRequest(Request):

    def __init__(
            self,
            limit: int = None,
            tag=None,
            ID: int = None,
            content: bytes = None,
            active: bool = None) -> None:
        super().__init__()

        self.limit = limit
        self.tag = tag
        self.ID = ID
        self.content = content
        self.active = active

        self._query = ""
        self._args = []

    def select_query(self):

        self._query += "SELECT * FROM note"

        self.__add_filter()

        if self.limit != None:
            self._args.append(self.limit)
            self._query += " " + "LIMIT %s"

        self._query += ";"

        return self.query()

    def create_query(self):

        self._query += "INSERT INTO note(content) VALUES(%s)"
        self._args.append(self.content)

        self._query += ";"

        return self.query()

    def delete_query(self) -> None:
        self._query += "DELETE FROM tag WHERE fk_note_id = %s;" + " " + \
            "DELETE FROM note WHERE note_id = %s"
        self._args.append(self.ID)
        self._args.append(self.ID)

        self._query += ";"

        return self.query()

    def query(self):
        return self._query, tuple(self._args)

    def update_query(self):
        self._query += "UPDATE note SET"

        if self.content != None and self.active != None:
            self._add_update_content()
            self._query += ", "
            self._add_update_active()
        else:
            self._add_update_content()
            self._add_update_active()

        self._args.append(self.ID)
        self._query += " " + "WHERE note_id = %s"

        self._query += ";"

        return self.query()

    def __add_filter(self):
        """ Filter Request """
        if self.ID != None and self.tag != None:
            self._add_id_query()
            self._query += " " + "AND"
            self._add_tag_query()
        else:
            self._add_id_query()
            self._add_tag_query()

    def _add_id_query(self):
        if self.ID != None:
            self._args.append(self.ID)
            self._query += " " + "WHERE note_id = %s"

    def _add_tag_query(self):
        if self.tag != None:
            self._args.append(self.tag)
            self._query += " " + \
                "WHERE note_id IN (SELECT fk_note_id name FROM tag WHERE name = %s)"

    def _add_update_content(self):
        if self.content != None:
            self._args.append(self.content)
            self._query += " " + "content = %s"

    def _add_update_active(self):
        if self.active != None:
            self._args.append(self.active)
            self._query += " " + "active = %s"
