"""Beerlog database session handler."""

from sqlmodel import SQLModel

from beerlog.models import engine

SQLModel.metadata.create_all(engine)
