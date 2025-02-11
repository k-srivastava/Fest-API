"""Fest user and mapping."""
from typing import Optional

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import operations
from db.core import DBUser, DBNotFoundError


class _UserBase(BaseModel):
    """Base user model."""
    first_name: str
    last_name: str
    email_address: str
    phone_number: Optional[str]
    mahe_registration_number: Optional[int]
    pass_id: Optional[int]


class User(_UserBase):
    """Actual user model with primary key."""
    id: int

    class Config:
        from_attributes = True


class UserCreate(_UserBase):
    """User creation model."""


class UserUpdate(_UserBase):
    """User update model."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    phone_number: Optional[int] = None
    mahe_registration_number: Optional[int] = None
    pass_id: Optional[int] = None


def read_db(user_id: int, session: Session) -> DBUser:
    """
    Read a user from the DB via its primary key.

    :param user_id: ID of the user to read.
    :type user_id: int
    :param session: Current DB session.
    :type session: Session

    :return: User DB instance.
    :rtype: DBUser

    :raise DBNotFoundError: User does not exist.
    """
    db_user: Optional[DBUser] = session.get(DBUser, user_id)

    if db_user is None:
        raise DBNotFoundError(f'User with ID {user_id} not found.')

    return db_user


def read_pass_db(user_id: int, session: Session) -> Optional[int]:
    """
    Read a user's pass from the DB via its primary key.

    :param user_id: ID of the user whose pass is to be read.
    :type user_id: int
    :param session: Current DB session.
    :type session: Session

    :return: User pass primary key, if it exists, else None.
    :rtype: Optional[int]

    :raise DBNotFoundError: User does not exist.
    """
    query = sqlalchemy.select(DBUser.pass_id).where(DBUser.id == user_id)
    pass_id = session.execute(query).scalar()

    if pass_id is None:
        raise DBNotFoundError(f'User with ID {user_id} not found.')

    return pass_id


def create_db(user: UserCreate, session: Session) -> DBUser:
    """
    Create a new user in the DB.

    :param user: User to create.
    :type user: UserCreate
    :param session: Current DB session.
    :type session: Session

    :return: New user DB instance.
    :rtype: DBUser
    """
    return operations.create_db(user, DBUser, session)


def update_db(user_id: int, user: UserUpdate, session: Session) -> DBUser:
    """
    Update an existing user in the DB.

    :param user_id: ID of the user to update.
    :type user_id: int
    :param user: User to update.
    :type user: UserUpdate
    :param session: Current DB session.
    :type session: Session

    :return: Updated user DB instance.
    :rtype: DBUser

    :raise DBNotFoundError: User does not exist.
    """
    return operations.update_db(user_id, user, read_db, session)


def delete_db(user_id: int, session: Session) -> DBUser:
    """
    Delete an existing user in the DB.

    :param user_id: ID of the user to delete.
    :type user_id: int
    :param session: Current DB session.
    :type session: Session

    :return: Deleted user DB instance.
    :rtype: DBUser

    :raise DBNotFoundError: User does not exist.
    """
    return operations.delete_db(user_id, read_db, session)
