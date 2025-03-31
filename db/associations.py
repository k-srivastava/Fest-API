"""Fest many-to-many associations."""
from typing import Optional, Sequence

import sqlalchemy
from sqlalchemy.orm import Session

from db.core import DBPassEvent, DBTeamUser, DBTeamEvent, DBTeam, DBNotFoundError, DBUser, DBValidationError, \
    DBUserEvent


def _validate_user_for_event(user_id: str, event_id: str, session: Session) -> bool:
    """
    Validate whether the user can access the event with their pass.

    :param user_id: ID of user to be validated.
    :type user_id: str
    :param event_id: ID of the event to be validated against.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: True if the user can access the event with their pass, else False.
    :rtype: bool

    :raise DBNotFoundError: User does not have a pass.
    """
    event_passes = read_event_passes_db(event_id, session)
    if len(event_passes) == 0:
        return True

    query = sqlalchemy.select(DBUser.pass_id).where(DBUser.id == user_id)
    user_pass_id = session.execute(query).scalar()

    if user_pass_id is None:
        raise DBNotFoundError(f'User with ID {user_id} does not have a pass.')

    return user_pass_id in event_passes


def _validate_team_users_for_event(team_id: str, event_id: str, host_only_access: bool, session: Session) -> bool:
    """
    Validate whether a team can access the event with their pass(es).

    :param team_id: ID of the team to be validated.
    :type team_id: str
    :param event_id: ID of the event to be validated against.
    :type event_id: str
    :param host_only_access: Whether only the host requires the relevant pass, or all team members.
    :type host_only_access: bool
    :param session: Current DB session.
    :type session: Session

    :return: True if the team can access the event with their pass(es), else False.
    :rtype: bool

    :raise DBNotFoundError: Team does not have a host or members do not have a pass.
    """
    query = sqlalchemy.select(DBTeam.host_id).where(DBTeam.id == team_id)
    host_id = session.execute(query).scalar()

    if host_id is None:
        raise DBNotFoundError(f'Team with ID {team_id} does not have a host.')

    event_passes = read_event_passes_db(event_id, session)
    if len(event_passes) == 0:
        return True

    query = sqlalchemy.select(DBUser.pass_id).where(DBUser.id == host_id)
    host_pass_id = session.execute(query).scalar()

    if host_pass_id is None:
        raise DBNotFoundError(f'Host with ID {host_id} of team with ID {team_id} does not have a pass.')

    host_pass_valid = host_pass_id in event_passes

    if host_only_access:
        return host_pass_valid

    team_member_ids = read_team_users_db(team_id, session)

    for team_member_id in team_member_ids:
        query = sqlalchemy.select(DBUser.pass_id).where(DBUser.id == team_member_id)
        team_member_pass_id = session.execute(query).scalar()

        if team_member_pass_id is None:
            raise DBNotFoundError(f'Member with ID {team_member_id} of team with ID {team_id} does not have a pass.')

        if team_member_pass_id not in event_passes:
            return False

    return True


# noinspection DuplicatedCode
def read_pass_events_db(pass_id: str, session: Session) -> Sequence[str]:
    """
    Read a pass' events from the DB via its primary key.

    :param pass_id: ID of the pass whose events are to be read.
    :type pass_id: str
    :param session: Current DB session.s
    :type session: Session

    :return: DB event IDs.
    :rtype: Sequence[str]
    """
    query = sqlalchemy.select(DBPassEvent.event_id).where(DBPassEvent.pass_id == pass_id)
    return session.execute(query).scalars().all()


def read_event_passes_db(event_id: str, session: Session) -> Sequence[str]:
    """
    Read an event's passes from the DB via its primary key.

    :param event_id: ID of the event whose passes are to be read.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: DB pass IDs.
    :rtype: Sequence[str]
    """
    query = sqlalchemy.select(DBPassEvent.pass_id).where(DBPassEvent.event_id == event_id)
    return session.execute(query).scalars().all()


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


# noinspection DuplicatedCode
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


def read_team_users_db(team_id: str, session: Session) -> Sequence[str]:
    """
    Read a team's members from the DB via its primary key.

    :param team_id: ID of the team whose members are to be read.
    :type team_id: str
    :param session: Current DB session.
    :type session: Session

    :return: DB user IDs.
    :rtype: Sequence[str]
    """
    query = sqlalchemy.select(DBTeamUser.user_id).where(DBTeamUser.team_id == team_id)
    return session.execute(query).scalars().all()


def read_user_teams_db(user_id: str, session: Session) -> Sequence[str]:
    """
    Read a user's teams of which they are a member from the DB via its primary key.

    :param user_id: ID of the user whose teams are to be read.
    :type user_id: str
    :param session: Current DB session.
    :type session: Session

    :return: DB team IDs.
    :rtype: Sequence[str]
    """
    query = sqlalchemy.select(DBTeamUser.team_id).where(DBTeamUser.user_id == user_id)
    return session.execute(query).scalars().all()


def create_team_user_db(team_id: str, user_id: str, validate: bool, session: Session) -> str:
    """
    Create a new team-user association in the DB.

    :param team_id: Team ID to associate with the user.
    :type team_id: str
    :param user_id: User ID to associate with the team.
    :type user_id: str
    :param validate: Validate whether the user is eligible for the events that they want to join the team for.
    :type validate: bool
    :param session: Current DB session.
    :type session: Session

    :return: New team-user association ID.
    :rtype: str

    :raise DBNotFoundError: User does not have a pass.
    :raise DBValidationError: User is not eligible to join the team.
    """
    if validate:
        event_ids = read_team_events_db(team_id, session)

        for event_id in event_ids:
            if not _validate_user_for_event(user_id, event_id, session):
                raise DBValidationError(
                    f'User with ID {user_id} cannot be added to team with ID {team_id} because they are not eligible '
                    f'for event with ID {event_id}.'
                )

    query = sqlalchemy.insert(DBTeamUser).values(team_id=team_id, user_id=user_id).returning(DBTeamUser.id)

    result = session.execute(query)
    new_id = result.scalar()
    session.commit()

    return new_id


# noinspection DuplicatedCode
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


def read_team_events_db(team_id: str, session: Session) -> Sequence[str]:
    """
    Read a team's events from the DB via its primary key.

    :param team_id: ID of the team whose events are to be read.
    :type team_id: str
    :param session: Current DB session.
    :type session: Session

    :return: DB event IDs.
    :rtype: Sequence[str]
    """
    query = sqlalchemy.select(DBTeamEvent.event_id).where(DBTeamEvent.team_id == team_id)
    return session.execute(query).scalars().all()


def read_event_teams_db(event_id: str, session: Session) -> Sequence[str]:
    """
    Read an event's registered teams from the DB via its primary key.

    :param event_id: ID of the event whose registered teams are to be read.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: DB team IDs.
    :rtype: Sequence[str]
    """
    query = sqlalchemy.select(DBTeamEvent.team_id).where(DBTeamEvent.event_id == event_id)
    return session.execute(query).scalars().all()


def create_team_event_db(
        team_id: str, event_id: str, validate: bool, validate_host_only: Optional[bool], session: Session
) -> str:
    """
    Create a new team-event association in the DB.

    :param team_id: Team ID to associate with the event.
    :type team_id: str
    :param event_id: Event ID to associate with the team.
    :type event_id: str
    :param validate: Validate whether the team's members are eligible for the events the team is registered for.
    :type validate: bool
    :param validate_host_only: If validate is True, then check if only the team host needs the required passes.
    :type validate_host_only: Optional[bool]
    :param session: Current DB session.
    :type session: Session

    :return: New team-event association ID.
    :rtype: str

    :raise DBNotFoundError: Team does not have a host or team members do not have a pass.
    :raise DBValidationError: Team is not eligible for the event.
    """
    if validate:
        if not _validate_team_users_for_event(team_id, event_id, validate_host_only, session):
            raise DBValidationError(
                f'Team with ID {team_id} cannot be added to event with ID {event_id} because team members do not have '
                'the valid passes.'
            )

    query = sqlalchemy.insert(DBTeamEvent).values(team_id=team_id, event_id=event_id).returning(DBTeamEvent.id)

    result = session.execute(query)
    new_id = result.scalar()
    session.commit()

    return new_id


# noinspection DuplicatedCode
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


def read_user_events_db(user_id: str, session: Session) -> Sequence[str]:
    """
    Read a user's events from the DB via its primary key.

    :param user_id: ID of the user whose events are to be read.
    :type user_id: str
    :param session: Current DB session.
    :type session: Session

    :return: DB event IDs.
    :rtype: Sequence[str]
    """
    query = sqlalchemy.select(DBUserEvent.event_id).where(DBUserEvent.user_id == user_id)
    return session.execute(query).scalars().all()


def read_event_users_db(event_id: str, session: Session) -> list[str]:
    """
    Read an event's registered users from the DB via its primary key.

    :param event_id: ID of the event whose registered users are to be read.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: List of registered user primary keys, if any, else empty list.
    :rtype: list[str]
    """
    query = sqlalchemy.select(DBUserEvent.user_id).where(DBUserEvent.event_id == event_id)
    user_ids = session.execute(query).scalars().all()

    return [user_id for user_id in user_ids] if user_ids is not None else []


def create_user_event_db(user_id: str, event_id: str, validate: bool, session: Session) -> str:
    """
    Create a new user-event association in the DB.

    :param user_id: User ID to associate with the event.
    :type user_id: str
    :param event_id: Event ID to associate with the user.
    :type event_id: str
    :param validate: Validate whether the user is eligible for the event.
    :type validate: bool
    :param session: Current DB session.
    :type session: Session

    :return: New user-event association ID.
    :rtype: str

    :raise DBNotFoundError: User does not have a pass.
    :raise DBValidationError: User is not eligible for the event.
    """
    if validate:
        if not _validate_user_for_event(user_id, event_id, session):
            raise DBValidationError(
                f'User with ID {user_id} cannot be added to event with ID {event_id} because of an invalid pass.'
            )

    query = sqlalchemy.insert(DBUserEvent).values(user_id=user_id, event_id=event_id).returning(DBUserEvent.id)

    result = session.execute(query)
    new_id = result.scalar()
    session.commit()

    return new_id


def delete_user_event_db(user_id: str, event_id: str, session: Session) -> str:
    """
    Delete an existing user-event association in the DB.

    :param user_id: User ID to disassociate from the event.
    :type user_id: str
    :param event_id: Event ID to disassociate from the user.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Deleted user-event association ID.
    :rtype: str
    """
    query = (
        sqlalchemy.delete(DBUserEvent)
        .where(DBUserEvent.user_id == user_id, DBUserEvent.event_id == event_id)
        .returning(DBUserEvent.id)
    )

    result = session.execute(query)
    deleted_id = result.scalar()
    session.commit()

    return deleted_id
