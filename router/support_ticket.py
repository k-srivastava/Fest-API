"""Route for all support tickets at /support-ticket."""
from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from typing_extensions import Optional

import router as router_core
from db import core, support_ticket
from db.core import DBNotFoundError, SupportTicketCategory
from db.support_ticket import SupportTicketCreate, SupportTicket, SupportTicketUpdate

router = APIRouter(prefix='/support-ticket', tags=['support_ticket'])


@router.get('/')
async def read_all_support_tickets(db: Session = Depends(core.get_db)) -> list[SupportTicket]:
    db_support_tickets = support_ticket.read_all_db(db)
    return [SupportTicket.model_validate(db_support_ticket) for db_support_ticket in db_support_tickets]


@router.post('/')
async def create_support_ticket(
        support_ticket_create: SupportTicketCreate, db: Session = Depends(core.get_db)
) -> SupportTicket:
    db_support_ticket = support_ticket.create_db(support_ticket_create, db)
    return SupportTicket.model_validate(db_support_ticket)


@router.get('/category/ids')
async def read_support_ticket_by_category(
        category: SupportTicketCategory, db: Session = Depends(core.get_db)
) -> Sequence[str]:
    db_support_ticket_ids = support_ticket.read_all_by_category(category, db)
    return db_support_ticket_ids


@router.get('/email_address/ids')
async def read_support_ticket_by_email_address(email_address: str, db: Session = Depends(core.get_db)) -> Sequence[str]:
    db_support_ticket_ids = support_ticket.read_all_by_email_address(email_address, db)
    return db_support_ticket_ids


@router.get('/{support_ticket_id}')
async def read_support_ticket(support_ticket_id: str, db: Session = Depends(core.get_db)) -> SupportTicket:
    try:
        db_support_ticket = support_ticket.read_db(support_ticket_id, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return SupportTicket.model_validate(db_support_ticket)


@router.post('/{support_ticket_id}')
async def solve_support_ticket(
        support_ticket_id: str, solved: bool, email_address: Optional[str] = None, db: Session = Depends(core.get_db)
) -> SupportTicket:
    if not solved and email_address is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email address provided for an unsolved support ticket. Use PATCH for manual updates instead.'
        )

    try:
        update_model = SupportTicketUpdate(solved=solved, solved_email_address=email_address)
        db_support_ticket = support_ticket.update_db(support_ticket_id, update_model, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return SupportTicket.model_validate(db_support_ticket)


@router.patch('/{support_ticket_id}')
async def update_support_ticket(
        support_ticket_id: str, support_ticket_update: SupportTicketUpdate, db: Session = Depends(core.get_db)
) -> SupportTicket:
    try:
        db_support_ticket = support_ticket.update_db(support_ticket_id, support_ticket_update, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return SupportTicket.model_validate(db_support_ticket)


@router.delete('/{support_ticket_id}')
async def delete_support_ticket(support_ticket_id: str, db: Session = Depends(core.get_db)) -> SupportTicket:
    try:
        db_support_ticket = support_ticket.delete_db(support_ticket_id, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return SupportTicket.model_validate(db_support_ticket)
