"""Fest user and mapping."""
from typing import Optional

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import operations
from db.core import DBUser, DBNotFoundError, DBTeam


class _UserBase(BaseModel):
    """Base user model."""
    first_name: str
    last_name: str
    email_address: str
    phone_number: Optional[str]
    mahe_registration_number: Optional[int]
    pass_id: Optional[str]


class User(_UserBase):
    """Actual user model with primary key."""
    id: str

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
    pass_id: Optional[str] = None


def read_db(user_id: str, session: Session) -> DBUser:
    """
    Read a user from the DB via its primary key.

    :param user_id: ID of the user to read.
    :type user_id: str
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


def read_id_db(user_email_address: str, session: Session) -> Optional[str]:
    """
    Read a user's ID from the DB via their unique email address.

    :param user_email_address: Email address of the user whose ID is to be read.
    :type user_email_address: str
    :param session: Current DB session.
    :type session: Session

    :return: User ID primary key, if it exists, else None.
    :rtype: Optional[str]

    :raise DBNotFoundError: User does not exist.
    """
    query = sqlalchemy.select(DBUser.id).where(DBUser.email_address == user_email_address)
    user_id = session.execute(query).scalar()

    if user_id is None:
        raise DBNotFoundError(f'User with email address {user_email_address} not found.')

    return user_id


def read_pass_db(user_id: str, session: Session) -> Optional[str]:
    """
    Read a user's pass from the DB via its primary key.

    :param user_id: ID of the user whose pass is to be read.
    :type user_id: str
    :param session: Current DB session.
    :type session: Session

    :return: User pass primary key, if it exists, else None.
    :rtype: Optional[str]

    :raise DBNotFoundError: User does not exist.
    """
    query = sqlalchemy.select(DBUser.pass_id).where(DBUser.id == user_id)
    pass_id = session.execute(query).scalar()

    if pass_id is None:
        raise DBNotFoundError(f'User with ID {user_id} not found.')

    return pass_id


def read_teams_host_db(user_id: str, session: Session) -> list[str]:
    """
    Read all the teams a user is a host of from the DB via the host's primary key.

    :param user_id: ID of the user whose teams are to be read.
    :type user_id: str
    :param session: Current DB session.
    :type session: Session

    :return: List of team primary keys, if any, else empty list.
    :rtype: list[str]
    """
    query = sqlalchemy.select(DBTeam.id).where(DBTeam.host_id == user_id)
    team_ids = session.execute(query).scalars().all()

    return [team_id for team_id in team_ids] if team_ids is not None else []


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


def update_db(user_id: str, user: UserUpdate, session: Session) -> DBUser:
    """
    Update an existing user in the DB.

    :param user_id: ID of the user to update.
    :type user_id: str
    :param user: User to update.
    :type user: UserUpdate
    :param session: Current DB session.
    :type session: Session

    :return: Updated user DB instance.
    :rtype: DBUser

    :raise DBNotFoundError: User does not exist.
    """
    return operations.update_db(user_id, user, read_db, session)


def delete_db(user_id: str, session: Session) -> DBUser:
    """
    Delete an existing user in the DB.

    :param user_id: ID of the user to delete.
    :type user_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Deleted user DB instance.
    :rtype: DBUser

    :raise DBNotFoundError: User does not exist.
    """
    return operations.delete_db(user_id, read_db, session)