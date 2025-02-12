"""Fest event type and mapping."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import operations
from db.core import EventType, DBEvent, DBNotFoundError


class _EventBase(BaseModel):
    """Base event model."""
    name: str
    description: Optional[str]
    type: EventType
    team_members: Optional[int]
    start: Optional[datetime]
    venue: Optional[str]


class Event(_EventBase):
    """Actual event model with primary key."""
    id: str

    class Config:
        from_attributes = True


class EventCreate(_EventBase):
    """Event creation model."""


class EventUpdate(_EventBase):
    """Event update model."""
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[EventType] = None
    team_members: Optional[int] = None
    start: Optional[datetime] = None
    venue: Optional[str] = None


def read_db(event_id: str, session: Session) -> DBEvent:
    """
    Read an event from the DB via its primary key.

    :param event_id: ID of the event to read.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Event DB instance.
    :rtype: DBEvent

    :raise DBNotFoundError: Event does not exist.
    """
    db_event: Optional[DBEvent] = session.get(DBEvent, event_id)

    if db_event is None:
        raise DBNotFoundError(f'Event with ID {event_id} not found.')

    return db_event


def read_all_db(session: Session) -> list[DBEvent]:
    """
    Read all events from the DB.

    :param session: Current DB session.
    :type session: Session

    :return: All event DB instances.
    :rtype: list[DBEvent]
    """
    # noinspection PyTypeChecker
    return session.query(DBEvent).all()


def create_db(event: EventCreate, session: Session) -> DBEvent:
    """
    Create a new event in the DB.

    :param event: Event to create.
    :type event: EventCreate
    :param session: Current DB session.
    :type session: Session

    :return: New event DB instance.
    :rtype: DBEvent
    """
    return operations.create_db(event, DBEvent, session)


def update_db(event_id: str, event: EventUpdate, session: Session) -> DBEvent:
    """
    Update an existing event in the DB.

    :param event_id: ID of the event to update.
    :type event_id: str
    :param event: Event to update.
    :type event: EventUpdate
    :param session: Current DB session.
    :type session: Session

    :return: Updated event DB instance.
    :rtype: DBEvent

    :raise DBNotFoundError: Event does not exist.
    """
    return operations.update_db(event_id, event, read_db, session)


def delete_db(event_id: str, session: Session) -> DBEvent:
    """
    Delete an existing event from the DB.

    :param event_id: ID of the event to delete.
    :type event_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Deleted event DB instance.
    :rtype: DBEvent

    :raise DBNotFoundError: Event does not exist.
    """
    return operations.delete_db(event_id, read_db, session)