"""Route for all events at /event."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from db import core, event
from db.core import DBNotFoundError
from db.event import EventCreate, Event, EventUpdate

router = APIRouter(prefix='/event', tags=['event'])


@router.get('/')
def read_all_events(db: Session = Depends(core.get_db)) -> list[Event]:
    db_events = event.read_all_db(db)
    return [Event.model_validate(db_event) for db_event in db_events]


@router.post('/')
def create_event(event_create: EventCreate, db: Session = Depends(core.get_db)) -> Event:
    db_event = event.create_db(event_create, db)
    return Event.model_validate(db_event)


@router.get('/{event_id}')
def read_event(event_id: str, db: Session = Depends(core.get_db)) -> Event:
    try:
        db_event = event.read_db(event_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Event.model_validate(db_event)


@router.patch('/{event_id}')
def update_event(event_id: str, event_update: EventUpdate, db: Session = Depends(core.get_db)) -> Event:
    try:
        db_event = event.update_db(event_id, event_update, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Event.model_validate(db_event)


@router.delete('/{event_id}')
def delete_event(event_id: str, db: Session = Depends(core.get_db)) -> Event:
    try:
        db_event = event.delete_db(event_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Event.model_validate(db_event)
