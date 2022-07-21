"""Beerlog database session handler."""

import warnings

from sqlalchemy.exc import SAWarning
from sqlmodel import Session, SQLModel
from sqlmodel.sql.expression import Select, SelectOfScalar

from beerlog.models import engine

warnings.filterwarnings("ignore", category=SAWarning)
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """
    Get service database session.

    Returns
    -------
    sqlmodel.orm.session.Session
        Session to manipulate service database.

    """
    return Session(engine)
