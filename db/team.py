"""Fest team and mapping."""
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import operations
from db.core import DBTeam, DBNotFoundError


class _TeamBase(BaseModel):
    """Base team model."""
    name: str
    host_id: str


class Team(_TeamBase):
    """Actual team model with primary key."""
    id: str

    class Config:
        from_attributes = True


class TeamCreate(_TeamBase):
    """Team creation model."""


class TeamUpdate(_TeamBase):
    """Team update model."""
    name: Optional[str] = None
    host_id: Optional[str] = None


def read_db(team_id: str, session: Session) -> DBTeam:
    """
    Read a team from the DB via its primary key.

    :param team_id: ID of the team to read.
    :type team_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Team DB instance.
    :rtype: DBTeam

    :raise DBNotFoundError: Team does not exist.
    """
    db_team: Optional[DBTeam] = session.get(DBTeam, team_id)

    if db_team is None:
        raise DBNotFoundError(f'Team with ID {team_id} not found.')

    return db_team


def create_db(team: TeamCreate, session: Session) -> DBTeam:
    """
    Create a new team in the DB.

    :param team: Team to create.
    :type team: TeamCreate
    :param session: Current DB session.
    :type session: Session

    :return: New team DB instance.
    :rtype: DBTeam
    """
    return operations.create_db(team, DBTeam, session)


def update_db(team_id: str, team: TeamUpdate, session: Session) -> DBTeam:
    """
    Update an existing team in the DB.

    :param team_id: ID of the team to update.
    :type team_id: str
    :param team: Team to update.
    :type team: TeamUpdate
    :param session: Current DB session.
    :type session: Session

    :return: Updated team DB instance.
    :rtype: DBTeam

    :raise DBNotFoundError: Team does not exist.
    """
    return operations.update_db(team_id, team, read_db, session)


def delete_db(team_id: str, session: Session) -> DBTeam:
    """
    Delete an existing team from the DB.

    :param team_id: ID of the team to delete.
    :type team_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Deleted team DB instance.
    :rtype: DBTeam

    :raise DBNotFoundError: Team does not exist.
    """
    return operations.delete_db(team_id, read_db, session)
