

from Note.cli.validators import _format_tags_callback
from Note.cli.utils import display_output
from Note.database.database import Database, NoteDatabase

from typing import List

import typer

app = typer.Typer(name="search", help="Search the database.")


@app.command(name="list")
def list_with_limit(
        limit: int = typer.Option(5, help="Limit Results."),
        active: bool = typer.Option(True, "-h", "--hidden", show_default=False, help="List hidden note's only")):
    """
    List notes

    Args:
        limit: Limits the output of search.
            >>> Note search list --limit 10

        active: Display hidden note's only.
            >>> Note search list -h
    """

    db = NoteDatabase(Database)

    results = db.select_note(limit, active=active)

    display_output(results)


@app.command(name="tag")
def list_with_limit_and_tag(
        tags: List[str] = typer.Option(
            ..., "-t", "--tag", show_default=False, help="A given tag to search.", callback=_format_tags_callback),
        limit: int = typer.Option(5, help="Limit Results."),
        active: bool = typer.Option(True, "-h", "--hidden", show_default=False, help="List hidden note's only")):
    """
    List notes by the given tags.

    Args:
        tags: list of tags to search.
            ` Note search tag -t test -t dev -t "Computer Science" `
        limit: Limits the output of search.
            ` Note search tag -t test --limit 10 `
        active: Display hidden note's only.
            ` Note search tag -t test -h `
    """

    db = NoteDatabase(Database)

    results = db.select_note_by_tags(tags=tags, limit=limit, active=active)

    display_output(results)


@ app.command(name="id")
def search_by_id(
    id_: int = typer.Argument(
        ..., metavar="id", help="Note to fetch.")):
    """
    Search by id.

    Args:
        id_: The id of the note to search. Ignores hidden status.
            ` Note search id 1 `
    """

    db = NoteDatabase(Database)

    result = db.select_note_by_id(id_)

    try:
        display_output([result])
    except AttributeError:
        error_message = typer.style(
            "ID %s could not be found!" % (id_), fg=typer.colors.YELLOW)
        typer.echo()
        typer.echo(error_message)
        typer.echo()
