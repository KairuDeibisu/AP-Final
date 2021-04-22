

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer, BLOB, Date, Boolean, String

import typer

Base = declarative_base()


class Note(Base):
    """
    Represents the note table in the database.
    """

    __tablename__ = "note"
    id_ = Column("id", Integer(), primary_key=True, autoincrement=True)
    content = Column("content", BLOB, nullable=False)
    date_ = Column("date", Date(), default=datetime.now(), nullable=True)
    active = Column("active", Boolean(), default=True, nullable=False)

    fk_note_id = relationship("Tag", order_by="Tag.fk_note_id", cascade="all, delete-orphan")


    def display(self):
        """
        Display note onto the console.
        """


        id_output= typer.style("ID:\t %s" % (self.id_), fg=typer.colors.YELLOW)
        typer.echo(id_output)
        typer.echo("Date:\t %s" % (self.date_))
        typer.echo("Active:\t %s" % (self.active))
        typer.echo()
        typer.echo("%s" % (self.content.decode("utf-8").strip()))
        typer.echo()

class Tag(Base):
    """
    Represents the tag table in the database.
    """
    
    __tablename__ = "tag"
    fk_note_id = Column("fk_note_id", Integer(), ForeignKey(Note.id_), primary_key=True)
    name = Column("name", String(255), primary_key=True)