"""Generate the DB schema and SQLAlchemy session for testing."""
from typing import Generator

import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import StaticPool, orm
from sqlalchemy.orm import Session

from db import core
from db.core import DBBase

_DATABASE_URL = 'sqlite:///:memory:'
_test_engine = sqlalchemy.create_engine(_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool)
_test_session_local = orm.sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


def get_test_db() -> Generator[Session, None, None]:
    """
    Get a current test DB session as a generator. The session is automatically closed after it is used.

    :return: The current test DB session.
    :rtype: Generator[Session, None, None]
    """
    db = _test_session_local()

    try:
        yield db
    finally:
        db.close()


def setup_tests(app: FastAPI):
    """
    Override the app production DB dependency with the test DB and create the schema.

    :param app: App in which the test DB dependency will be overridden.
    :type app: FastAPI
    """
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[core.get_db] = get_test_db
    DBBase.metadata.create_all(bind=_test_engine)


def teardown_tests():
    """Drop all tables from the schema."""
    DBBase.metadata.drop_all(bind=_test_engine)
