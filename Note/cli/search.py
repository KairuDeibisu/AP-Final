
from Note.cli.validators import _format_tags_callback

from typing import Optional, List
import logging

import typer

logger = logging.getLogger(__name__)

app = typer.Typer(name="search", help="Search the database.")


@app.command(name="list")
class Search:
    """
    Display Notes.
    """

    def __init__(
        self,
        limit: int = typer.Option(
            5, help="Limit Results.")):

        self.limit = limit

        logger.info(f"limit: {self.limit}")


@app.command(name="tag")
class TagSearch(Search):
    """
    Search by tags.
    """

    def __init__(
        self,
        tags: List[str] = typer.Argument(
            ..., callback=_format_tags_callback),
        limit: int = typer.Option(
            5, help="Limit Results.")):
        super().__init__(limit)

        self.tags = tags

        logger.info(f"Tags: {self.tags}")


@app.command(name="id")
def search_by_id(
    id_: int = typer.Argument(
        ..., metavar="id", help="Note to fetch.")):
    """
    Search by id.
    """

    logger.info(f"ID: {id_}")
