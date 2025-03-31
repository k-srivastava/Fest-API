"""Fest pass type and mapping."""
from decimal import Decimal
from typing import Optional, Sequence

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import operations
from db.core import DBPass, DBNotFoundError


class _PassBase(BaseModel):
    """Base pass model."""
    name: str
    description: Optional[str]
    cost: Decimal


class Pass(_PassBase):
    """Actual pass model with primary key."""
    id: str

    class Config:
        from_attributes = True


class PassCreate(_PassBase):
    """Pass creation model."""


class PassUpdate(_PassBase):
    """Pass update model."""
    name: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[Decimal] = None


def read_db(pass_id: str, session: Session) -> DBPass:
    """
    Read a pass from the DB via its primary key.

    :param pass_id: ID of the pass to read.
    :type pass_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Pass DB instance.
    :rtype: DBPass

    :raise DBNotFoundError: Pass does not exist.
    """
    db_pass: Optional[DBPass] = session.get(DBPass, pass_id)

    if db_pass is None:
        raise DBNotFoundError(f'Pass with ID {pass_id} not found.')

    return db_pass


def read_by_ids_db(pass_ids: Sequence[str], session: Session) -> Sequence[DBPass]:
    """
    Read all events from the DB via their primary keys.

    :param pass_ids: IDs of the passes to be read.
    :type pass_ids: Sequence[str]
    :param session: Current DB session.
    :type session: Session

    :return: Pass DB instances.
    :rtype: Sequence[DBPass]
    """
    query = sqlalchemy.select(DBPass).where(DBPass.id.in_(pass_ids))
    return session.execute(query).scalars().all()


def read_all_db(session: Session) -> list[DBPass]:
    """
    Read all passes from the DB.

    :param session: Current DB session.
    :type session: Session

    :return: All pass DB instances.
    :rtype: list[DBPass]
    """
    # noinspection PyTypeChecker
    return session.query(DBPass).all()


def create_db(pass_: PassCreate, session: Session) -> DBPass:
    """
    Create a new pass in the DB.

    :param pass_: Pass to create.
    :type pass_: PassCreate
    :param session: Current DB session.
    :type session: Session

    :return: New pass DB instance.
    :rtype: DBPass
    """
    return operations.create_db(pass_, DBPass, session)


def update_db(pass_id: str, pass_: PassUpdate, session: Session) -> DBPass:
    """
    Update an existing pass in the DB.

    :param pass_id: ID of the pass to update.
    :type pass_id: str
    :param pass_: Pass to update.
    :type pass_: PassUpdate
    :param session: Current DB session.
    :type session: Session

    :return: Updated pass DB instance.
    :rtype: DBPass

    :raise DBNotFoundError: Pass does not exist.
    """
    return operations.update_db(pass_id, pass_, read_db, session)


def delete_db(pass_id: str, session: Session) -> DBPass:
    """
    Delete an existing pass from the DB.

    :param pass_id: ID of the pass to delete.
    :type pass_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Deleted pass DB instance.
    :rtype: DBPass

    :raise DBNotFoundError: Pass does not exist.
    """
    return operations.delete_db(pass_id, read_db, session)
