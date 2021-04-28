

from Note.cli.validators import _format_tags_callback
from Note.cli.search import search_by_id
from Note.cli.utils import display_output
from Note.database.database import NoteDatabase, Database
from Note.database.table import Note as NoteTable

from enum import Enum
from typing import List, Optional, Tuple
import os
import tempfile
import subprocess

import typer

app = typer.Typer(name="manage", help="Manage the database.")

FILENAME = "tmp_note"
FILEPATH = os.path.join(tempfile.gettempdir(), FILENAME)


class Editor:
    editors = []

    def __init__(self, name: str, args: Tuple):
        self.name = name
        self.args = args
        self.editors.append(self)

    def __eq__(self, b):
        return self.name == b

    def __repr__(self):
        return self.name


class EditorChoice(str, Enum):
    vim = str(Editor("vim", ("vim", "-n", FILEPATH)))
    nano = str(Editor("nano", ("nano", FILEPATH)))


@app.command()
def create(
        message: Optional[str] = typer.Option(
            None, "-m", "--message", show_default=False, help="Message to add to the database."),
        tags: Optional[List[str]] = typer.Option(
            None, "-t", "--tags", show_default=False, help="Tags to organize message.", callback=_format_tags_callback),
        editor: EditorChoice = typer.Option(
            "vim", show_choices=True, help="Supported editors.")):
    """
    Insert note into the database.
    """

    message = message if message else get_message_from_editor(editor)

    db = NoteDatabase(Database)

    db.insert_note(NoteTable(content=message.encode("utf-8")))

    note = db.select_note_by_id(db.last_row_id)

    db.insert_tag(note.id_, set(tags))

    search_by_id(db.last_row_id)




@app.command()
def remove(
    id_: int = typer.Argument(
        ..., metavar="id", help="The id of the note to hide/delete from list."),
    delete: bool = typer.Option(
        False, show_default=False, confirmation_prompt=True, help="Delete note from list forever.")):
    """
    Hide or Delete note from database.
    """
    
    db = NoteDatabase(Database)
    
    if delete:
        db.delete_note(id_)
    else:
        db.set_note_active_value(id_, False)
        result = db.select_note_by_id(id_,)

        display_output([result])

@app.command()
def recover(
    id_: int = typer.Argument(
        ..., metavar="id", help="The id of the note to recover."),
        ):
    """
    Restore hidden note.
    """

    db = NoteDatabase(Database)

    db.set_note_active_value(id_, value=True)

    result = db.select_note_by_id(id_)

    display_output([result])

def get_message_from_editor(selected_editor: str) -> str:
    """
    Launch editor and get a note message.
    """

    for editor in Editor.editors:
        if editor == selected_editor:

            process = subprocess.run(" ".join(editor.args), shell=True)

            if process.returncode:
                raise Exception(f"{editor} not installed!")

            return _read_message()

    raise NotImplementedError(f"editor: {selected_editor} not implemented.")


def _read_message() -> str:
    """

    Read message from tmp file.

    Returns:
        data: test in message file.
    """

    try:
        with open(FILEPATH, "r") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        typer.echo("Aborting!")
        typer.Exit(1)
    finally:
        _remove_tmp_file()


def _remove_tmp_file():
    """
    Cleans up tmp file.
    """

    try:
        os.remove(FILEPATH)
    except FileNotFoundError:
        pass
