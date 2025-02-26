"""Route for all support tickets at /support-ticket."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from typing_extensions import Optional

from db import core, support_ticket
from db.core import DBNotFoundError
from db.support_ticket import SupportTicketCreate, SupportTicket, SupportTicketUpdate

router = APIRouter(prefix='/support-ticket', tags=['support_ticket'])


@router.post('/')
def create_support_ticket(
        support_ticket_create: SupportTicketCreate, db: Session = Depends(core.get_db)
) -> SupportTicket:
    db_support_ticket = support_ticket.create_db(support_ticket_create, db)
    return SupportTicket.model_validate(db_support_ticket)


@router.get('/{support_ticket_id}')
def read_support_ticket(support_ticket_id: str, db: Session = Depends(core.get_db)) -> SupportTicket:
    try:
        db_support_ticket = support_ticket.read_db(support_ticket_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return SupportTicket.model_validate(db_support_ticket)


@router.post('/{support_ticket_id}')
def solve_support_ticket(
        support_ticket_id: str, solved: bool, email_address: Optional[str] = None, db: Session = Depends(core.get_db)
) -> SupportTicket:
    if not solved and email_address is not None:
        raise HTTPException(
            status_code=400,
            detail='Email address provided for an unsolved support ticket. Use PATCH for manual updates instead.'
        )

    try:
        update_model = SupportTicketUpdate(solved=solved, solved_email_address=email_address)
        db_support_ticket = support_ticket.update_db(support_ticket_id, update_model, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return SupportTicket.model_validate(db_support_ticket)


@router.patch('/{support_ticket_id}')
def update_support_ticket(
        support_ticket_id: str, support_ticket_update: SupportTicketUpdate, db: Session = Depends(core.get_db)
) -> SupportTicket:
    try:
        db_support_ticket = support_ticket.update_db(support_ticket_id, support_ticket_update, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return SupportTicket.model_validate(db_support_ticket)


@router.delete('/{support_ticket_id}')
def delete_support_ticket(support_ticket_id: str, db: Session = Depends(core.get_db)) -> SupportTicket:
    try:
        db_support_ticket = support_ticket.delete_db(support_ticket_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return SupportTicket.model_validate(db_support_ticket)
