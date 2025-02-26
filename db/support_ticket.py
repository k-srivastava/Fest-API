"""Fest support ticket and mapping."""
from datetime import datetime
from typing import Optional

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
