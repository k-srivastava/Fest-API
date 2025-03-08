"""Fest support ticket and mapping."""
from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import operations
from db.core import SupportTicketCategory, DBSupportTicket, DBNotFoundError


class _SupportTicketBase(BaseModel):
    """Base support ticket model."""
    name: str
    description: str
    category: SupportTicketCategory
    timestamp: datetime
    solved: bool
    college_name: Optional[str]
    email_address: Optional[str]
    phone_number: Optional[str]
    solved_email_address: Optional[str]
    comment: Optional[str]


class SupportTicket(_SupportTicketBase):
    """Actual support ticket model with primary key."""
    id: str

    class Config:
        from_attributes = True


class SupportTicketCreate(_SupportTicketBase):
    """Support ticket creation model."""


class SupportTicketUpdate(_SupportTicketBase):
    """Support ticket update model."""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[SupportTicketCategory] = None
    timestamp: Optional[datetime] = None
    solved: Optional[bool] = None
    college_name: Optional[str] = None
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    solved_email_address: Optional[str] = None
    comment: Optional[str] = None


def read_db(support_ticket_id: str, session: Session) -> DBSupportTicket:
    """
    Read a support ticket from the DB via its primary key.

    :param support_ticket_id: ID of the support ticket to read.
    :type support_ticket_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Support ticket DB instance.
    :rtype: DBSupportTicket

    :raise DBNotFoundError: Support ticket does not exist.
    """
    db_support_ticket: Optional[DBSupportTicket] = session.get(DBSupportTicket, support_ticket_id)

    if db_support_ticket is None:
        raise DBNotFoundError(f'Support ticket with ID {support_ticket_id} not found.')

    return db_support_ticket


def read_all_db(session: Session) -> list[DBSupportTicket]:
    """
    Read all support tickets from the DB.

    :param session: Current DB session.
    :type session: Session

    :return: All support ticket DB instances.
    :rtype: list[DBSupportTicket]
    """
    # noinspection PyTypeChecker
    return session.query(DBSupportTicket).all()


def read_all_by_email_address(email_address: str, session: Session) -> list[str]:
    """
    Read all the support ticket IDs from the DB with the given email address.

    :param email_address: Email address of the support ticket to be read.
    :type email_address: str
    :param session: Current DB session.
    :type session: Session

    :return: List of DB support ticket IDs, if any, else empty list.
    :rtype: list[str]
    """
    query = sqlalchemy.select(DBSupportTicket.id).where(DBSupportTicket.email_address == email_address)
    db_support_ticket_ids = session.execute(query).scalars().all()

    if db_support_ticket_ids is None:
        return []

    return [db_support_ticket_id for db_support_ticket_id in db_support_ticket_ids]


def read_all_by_category(category: SupportTicketCategory, session: Session) -> list[str]:
    """
    Read all the support ticket IDs from the DB with the given category.

    :param category: Category of the support ticket to be read.
    :type category: SupportTicketCategory
    :param session: Current DB session.
    :type session: Session

    :return: List of DB support ticket IDs, if any, else empty list.
    :rtype: list[str]
    """
    query = sqlalchemy.select(DBSupportTicket.id).where(DBSupportTicket.category == category)
    db_support_ticket_ids = session.execute(query).scalars().all()

    if db_support_ticket_ids is None:
        return []

    return [db_support_ticket_id for db_support_ticket_id in db_support_ticket_ids]


def create_db(support_ticket: SupportTicketCreate, session: Session) -> DBSupportTicket:
    """
    Create a new support ticket in the DB.

    :param support_ticket: Support ticket to create.
    :type support_ticket: SupportTicketCreate
    :param session: Current DB session.
    :type session: Session

    :return: New support ticket DB instance.
    :rtype: DBSupportTicket
    """
    return operations.create_db(support_ticket, DBSupportTicket, session)


def update_db(support_ticket_id: str, support_ticket: SupportTicketUpdate, session: Session) -> DBSupportTicket:
    """
    Update an existing support ticket in the DB.

    :param support_ticket_id: ID of the support ticket to update.
    :type support_ticket_id: str
    :param support_ticket: Support ticket to update.
    :type support_ticket: SupportTicket
    :param session: Current DB session.
    :type session: Session

    :return: Updated support ticket DB instance.
    :rtype: DBSupportTicket

    :raise DBNotFoundError: Support ticket does not exist.
    """
    return operations.update_db(support_ticket_id, support_ticket, read_db, session)


def delete_db(support_ticket_id: str, session: Session) -> DBSupportTicket:
    """
    Delete an existing support ticket from the DB.

    :param support_ticket_id: ID of the support ticket to delete.
    :type support_ticket_id: str
    :param session: Current DB session.
    :type session: Session

    :return: Deleted support ticket DB instance.
    :rtype: DBSupportTicket

    :raise DBNotFoundError: Support ticket does not exist.
    """
    return operations.delete_db(support_ticket_id, read_db, session)
