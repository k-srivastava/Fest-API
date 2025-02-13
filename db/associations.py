"""Fest many-to-many associations."""
import sqlalchemy
from sqlalchemy.orm import Session

from db.core import DBPassEvent, DBTeamUser, DBTeamEvent


# noinspection DuplicatedCode
def read_pass_events_db(pass_id: str, session: Session) -> list[str]:
    """
    Read a pass' events from the DB via its primary key.

    :param pass_id: ID of the pass whose events are to be read.
    :type pass_id: str
    :param session: Current DB session.s
    :type session: Session

    :return: List of event primary keys, if any, else empty list.
    :rtype: list[str]
    """
    query = sqlalchemy.select(DBPassEvent.event_id).where(DBPassEvent.pass_id == pass_id)
    event_ids = session.execute(query).scalars().all()

    return [event_id for event_id in event_ids] if event_ids is not None else []


def read_event_passes_db(event_id: str, session: Session) -> list[str]:
    """
    Read an event's passes from the DB via its primary key.

    :param event_id: ID of the event whose passes are to be read.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: List of pass primary keys, if any, else empty list.
    :rtype: list[str]
    """
    query = sqlalchemy.select(DBPassEvent.pass_id).where(DBPassEvent.event_id == event_id)
    pass_ids = session.execute(query).scalars().all()

    return [pass_id for pass_id in pass_ids] if pass_ids is not None else []


def create_pass_event_db(pass_id: str, event_id: str, session: Session) -> str:
    """
    Create a new pass-event association in the DB.

    :param pass_id: Pass ID to associate with the event.
    :type pass_id: str
    :param event_id: Event ID to associate with the pass.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: New pass-event association ID.
    :rtype: str
    """
    query = sqlalchemy.insert(DBPassEvent).values(pass_id=pass_id, event_id=event_id).returning(DBPassEvent.id)

    result = session.execute(query)
    new_id = result.scalar()
    session.commit()

    return new_id


def delete_pass_event_db(pass_id: str, event_id: str, session: Session) -> str:
    """
    Delete an existing pass-event association in the DB.

    :param pass_id: Pass ID to disassociate from the event.
    :type pass_id: str
    :param event_id: Event ID to disassociate from the pass.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Deleted pass-event association ID.
    :rtype: str
    """
    query = (
        sqlalchemy.delete(DBPassEvent)
        .where(DBPassEvent.pass_id == pass_id, DBPassEvent.event_id == event_id)
        .returning(DBPassEvent.id)
    )

    result = session.execute(query)
    deleted_id = result.scalar()
    session.commit()

    return deleted_id


# noinspection DuplicatedCode
def read_team_users_db(team_id: str, session: Session) -> list[str]:
    """
    Read a team's members from the DB via its primary key.

    :param team_id: ID of the team whose members are to be read.
    :type team_id: str
    :param session: Current DB session.
    :type session: Session

    :return: List of user member primary keys, if any, else empty list.
    :rtype: list[str]
    """
    query = sqlalchemy.select(DBTeamUser.user_id).where(DBTeamUser.team_id == team_id)
    user_ids = session.execute(query).scalars().all()

    return [user_id for user_id in user_ids] if user_ids is not None else []


def create_team_user_db(team_id: str, user_id: str, session: Session) -> str:
    """
    Create a new team-user association in the DB.

    :param team_id: Team ID to associate with the user.
    :type team_id: str
    :param user_id: User ID to associate with the team.
    :type user_id: str
    :param session: Current DB session.
    :type session: Session

    :return: New team-user association ID.
    :rtype: str
    """
    query = sqlalchemy.insert(DBTeamUser).values(team_id=team_id, user_id=user_id).returning(DBTeamUser.id)

    result = session.execute(query)
    new_id = result.scalar()
    session.commit()

    return new_id


def delete_team_user_db(team_id: str, user_id: str, session: Session) -> str:
    """
    Delete an existing team-user association in the DB.

    :param team_id: Team ID to disassociate from the user.
    :type team_id: str
    :param user_id: User ID to disassociate from the team.
    :type user_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Deleted team-user association ID.
    :rtype: str
    """
    query = (
        sqlalchemy.delete(DBTeamUser)
        .where(DBTeamUser.team_id == team_id, DBTeamUser.user_id == user_id)
        .returning(DBTeamUser.id)
    )

    result = session.execute(query)
    deleted_id = result.scalar()
    session.commit()

    return deleted_id


# noinspection DuplicatedCode
def read_team_events_db(team_id: str, session: Session) -> list[str]:
    """
    Read a team's events from the DB via its primary key.

    :param team_id: ID of the team whose events are to be read.
    :type team_id: str
    :param session: Current DB session.
    :type session: Session

    :return: List of event primary keys, if any, else empty list.
    :rtype: list[str]
    """
    query = sqlalchemy.select(DBTeamEvent.event_id).where(DBTeamEvent.team_id == team_id)
    event_ids = session.execute(query).scalars().all()

    return [event_id for event_id in event_ids] if event_ids is not None else []


def read_event_teams_db(event_id: str, session: Session) -> list[str]:
    """
    Read an event's registered teams from the DB via its primary key.

    :param event_id: ID of the event whose registered teams are to be read.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: List of registered team primary keys, if any, else empty list.
    :rtype: list[str]
    """
    query = sqlalchemy.select(DBTeamEvent.team_id).where(DBTeamEvent.event_id == event_id)
    team_ids = session.execute(query).scalars().all()

    return [team_id for team_id in team_ids] if team_ids is not None else []


def create_team_event_db(team_id: str, event_id: str, session: Session) -> str:
    """
    Create a new team-event association in the DB.

    :param team_id: Team ID to associate with the event.
    :type team_id: str
    :param event_id: Event ID to associate with the team.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: New team-event association ID.
    :rtype: str
    """
    query = sqlalchemy.insert(DBTeamEvent).values(team_id=team_id, event_id=event_id).returning(DBTeamEvent.id)

    result = session.execute(query)
    new_id = result.scalar()
    session.commit()

    return new_id


def delete_team_event_db(team_id: str, event_id: str, session: Session) -> str:
    """
    Delete an existing team-event association in the DB.

    :param team_id: Team ID to disassociate from the event.
    :type team_id: str
    :param event_id: Event ID to disassociate from the team.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Deleted team-event association ID.
    :rtype: str
    """
    query = (
        sqlalchemy.delete(DBTeamEvent)
        .where(DBTeamEvent.team_id == team_id, DBTeamEvent.event_id == event_id)
        .returning(DBTeamEvent.id)
    )

    result = session.execute(query)
    deleted_id = result.scalar()
    session.commit()

    return deleted_id
