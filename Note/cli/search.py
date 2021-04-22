
from Note.cli.validators import _format_tags_callback
from Note.database.database import Database, NoteDatabase

from typing import Optional, List
import logging

import typer

logger = logging.getLogger(__name__)

app = typer.Typer(name="search", help="Search the database.")


@app.command(name="list")
def list_with_limit(limit: int = typer.Option(5, help="Limit Results.")):
    """
    List notes
    """
    
    logger.info(f"limit: {limit}")
    db = NoteDatabase(Database)

    results = db.select_note(limit)

    if not results:
        error_message = typer.style("Can't find any results!", fg=typer.colors.YELLOW)
        typer.echo()
        typer.echo(error_message)
        typer.echo()
        typer.Exit(1)

    for result in results:
        result.display()
        
@app.command(name="tag")
def list_with_limit(
    tags: List[str] = typer.Option(
            ..., "-t", "--tags", show_default=False, help="Tags to organize message.", callback=_format_tags_callback),
    limit: int = typer.Option(5, help="Limit Results.")):
    """
    List notes
    """
    
    logger.info(f"limit: {limit}")
    logger.info(f"Tags: {tags}")
    db = NoteDatabase(Database)

    results = db.select_note_by_tags(tags, limit)

    if not results:
        error_message = typer.style("Can't find any results!", fg=typer.colors.YELLOW)
        typer.echo()
        typer.echo(error_message)
        typer.echo()
        typer.Exit(1)

    for result in results:
        result.display()



@app.command(name="id")
def search_by_id(
    id_: int = typer.Argument(
        ..., metavar="id", help="Note to fetch.")):
    """
    Search by id.
    """

    logger.info(f"ID: {id_}")

    db = NoteDatabase(Database)

    note = db.select_note_by_id(id_)

    try:
        note.display()
    except AttributeError:
        error_message = typer.style("ID %s could not be found!" % (id_), fg=typer.colors.YELLOW)
        typer.echo()
        typer.echo(error_message)
        typer.echo()
    
