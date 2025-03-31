"""Route for all passes at /pass."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

import router as router_core
from db import associations, core, event, pass_
from db.core import DBNotFoundError
from db.event import Event
from db.pass_ import Pass, PassCreate, PassUpdate

router = APIRouter(prefix='/pass', tags=['pass'])


@router.get('/')
async def read_all_passes(db: Session = Depends(core.get_db)) -> list[Pass]:
    db_passes = pass_.read_all_db(db)
    return [Pass.model_validate(db_pass) for db_pass in db_passes]


@router.post('/')
async def create_pass(pass_create: PassCreate, db: Session = Depends(core.get_db)) -> Pass:
    db_pass = pass_.create_db(pass_create, db)
    return Pass.model_validate(db_pass)


@router.get('/{pass_id}')
async def read_pass(pass_id: str, db: Session = Depends(core.get_db)) -> Pass:
    try:
        db_pass = pass_.read_db(pass_id, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return Pass.model_validate(db_pass)


@router.get('/{pass_id}/events')
async def read_pass_events(pass_id: str, db: Session = Depends(core.get_db)) -> list[Event]:
    try:
        event_ids = associations.read_pass_events_db(pass_id, db)
        db_events = event.read_by_ids_db(event_ids, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return [Event.model_validate(db_event) for db_event in db_events]


@router.post('/{pass_id}/events/{event_id}')
async def create_pass_event(pass_id: str, event_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    association_id = associations.create_pass_event_db(pass_id, event_id, db)
    return JSONResponse(content={'id': association_id}, status_code=status.HTTP_200_OK)


@router.delete('/{pass_id}/events/{event_id}')
async def delete_pass_event(pass_id: str, event_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    association_id = associations.delete_pass_event_db(pass_id, event_id, db)
    return JSONResponse(content={'id': association_id}, status_code=status.HTTP_200_OK)


@router.patch('/{pass_id}')
async def update_pass(pass_id: str, pass_update: PassUpdate, db: Session = Depends(core.get_db)) -> Pass:
    try:
        db_pass = pass_.update_db(pass_id, pass_update, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return Pass.model_validate(db_pass)


@router.delete('/{pass_id}')
async def delete_pass(pass_id: str, db: Session = Depends(core.get_db)) -> Pass:
    try:
        db_pass = pass_.delete_db(pass_id, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return Pass.model_validate(db_pass)
