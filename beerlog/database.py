"""Beerlog database session handler."""

import warnings

from sqlalchemy.exc import SAWarning
from sqlmodel import Session, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from beerlog import models
from beerlog.config import get_database_engine

warnings.filterwarnings("ignore", category=SAWarning)
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

engine = create_engine(get_database_engine())

models.SQLModel.metadata.create_all(engine)  # type: ignore


def get_session() -> Session:
    """
    Get service database session.

    Returns
    -------
    sqlmodel.orm.session.Session
        Session to manipulate service database.

    """
    return Session(engine)
