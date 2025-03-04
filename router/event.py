"""Route for all events at /event."""
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from db import associations, core, event, pass_, team
from db.core import DBNotFoundError, DBValidationError
from db.event import EventCreate, Event, EventUpdate
from db.pass_ import Pass
from db.team import Team

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


@router.get('/{event_id}/passes')
def read_event_passes(event_id: str, db: Session = Depends(core.get_db)) -> list[Pass]:
    try:
        pass_ids = associations.read_event_passes_db(event_id, db)
        db_passes = [pass_.read_db(pass_id, db) for pass_id in pass_ids]

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return [Pass.model_validate(db_pass) for db_pass in db_passes]


@router.post('/{event_id}/passes/{pass_id}')
def create_event_pass(event_id: str, pass_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    association_id = associations.create_pass_event_db(pass_id, event_id, db)
    return JSONResponse(content={'id': association_id}, status_code=200)


@router.delete('/{event_id}/passes/{pass_id}')
def delete_event_pass(event_id: str, pass_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    association_id = associations.delete_pass_event_db(pass_id, event_id, db)
    return JSONResponse(content={'id': association_id}, status_code=200)


@router.get('/{event_id}/teams')
def read_event_teams(event_id: str, db: Session = Depends(core.get_db)) -> list[Team]:
    try:
        team_ids = associations.read_event_teams_db(event_id, db)
        db_teams = [team.read_db(team_id, db) for team_id in team_ids]

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return [Team.model_validate(db_team) for db_team in db_teams]


@router.post('/{event_id}/teams/{team_id}')
def create_event_team(
        event_id: str, team_id: str, validate: bool = True, validate_host_only: Optional[bool] = False,
        db: Session = Depends(core.get_db)
) -> JSONResponse:
    try:
        association_id = associations.create_team_event_db(team_id, event_id, validate, validate_host_only, db)

    except DBValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return JSONResponse(content={'id': association_id}, status_code=200)


@router.delete('/{event_id}/teams/{team_id}')
def delete_event_team(event_id: str, team_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    association_id = associations.delete_team_event_db(team_id, event_id, db)
    return JSONResponse(content={'id': association_id}, status_code=200)


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
