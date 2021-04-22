

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer, BLOB, Date, Boolean, String


Base = declarative_base()


class Note(Base):
    """
    Represents the note table in the database.
    """

    __tablename__ = "note"
    id_ = Column("id", Integer(), primary_key=True, autoincrement=True)
    content = Column("content", BLOB, nullable=False)
    tags = Column("tags", String(255), nullable=True)
    date_ = Column("date", Date(), default=datetime.now(), nullable=True)
    active = Column("active", Boolean(), default=True, nullable=False)
