"""Route for all teams at /team."""
from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from db import associations, core, event, team, user
from db.core import DBNotFoundError, DBValidationError
from db.event import Event
from db.team import TeamCreate, Team, TeamUpdate
from db.user import User

router = APIRouter(prefix='/team', tags=['team'])


@router.get('/')
def read_all_teams(db: Session = Depends(core.get_db)) -> list[Team]:
    db_teams = team.read_all_db(db)
    return [Team.model_validate(db_team) for db_team in db_teams]


@router.post('/')
def create_team(team_create: TeamCreate, db: Session = Depends(core.get_db)) -> Team:
    db_team = team.create_db(team_create, db)
    return Team.model_validate(db_team)


@router.get('/{team_id}')
def read_team(team_id: str, db: Session = Depends(core.get_db)) -> Team:
    try:
        db_team = team.read_db(team_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Team.model_validate(db_team)


@router.get('/{team_id}/events')
def read_team_events(team_id: str, db: Session = Depends(core.get_db)) -> list[Event]:
    try:
        event_ids = associations.read_team_events_db(team_id, db)
        db_events = [event.read_db(event_id, db) for event_id in event_ids]

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return [Event.model_validate(db_event) for db_event in db_events]


@router.post('/{team_id}/events/{event_id}')
def create_team_event(
        team_id: str, event_id: str, validate: bool = True, validate_host_only: Optional[bool] = False,
        db: Session = Depends(core.get_db)
) -> JSONResponse:
    try:
        association_id = associations.create_team_event_db(team_id, event_id, validate, validate_host_only, db)

    except DBValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return JSONResponse(content={'id': association_id}, status_code=200)


@router.delete('/{team_id}/events/{event_id}')
def delete_team_event(team_id: str, event_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    association_id = associations.delete_team_event_db(team_id, event_id, db)
    return JSONResponse(content={'id': association_id}, status_code=200)


@router.get('/{team_id}/users')
def read_team_users(team_id: str, db: Session = Depends(core.get_db)) -> list[User]:
    try:
        user_ids = associations.read_team_users_db(team_id, db)
        db_users = [user.read_db(user_id, db) for user_id in user_ids]

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return [User.model_validate(db_user) for db_user in db_users]


@router.post('/{team_id}/users/{user_id}')
def create_team_user(team_id: str, user_id: str, validate: bool = True,
                     db: Session = Depends(core.get_db)) -> JSONResponse:
    try:
        association_id = associations.create_team_user_db(team_id, user_id, validate, db)

    except DBValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return JSONResponse(content={'id': association_id}, status_code=200)


@router.delete('/{team_id}/users/{user_id}')
def delete_team_user(team_id: str, user_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    if team.read_db(team_id, db).host_id == user_id:
        raise HTTPException(status_code=403, detail='Cannot delete host of team.')

    association_id = associations.delete_team_user_db(team_id, user_id, db)
    return JSONResponse(content={'id': association_id}, status_code=200)


@router.patch('/{team_id}')
def update_team(team_id: str, team_update: TeamUpdate, db: Session = Depends(core.get_db)) -> Team:
    try:
        db_team = team.update_db(team_id, team_update, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Team.model_validate(db_team)


@router.delete('/{team_id}')
def delete_team(team_id: str, db: Session = Depends(core.get_db)) -> Team:
    try:
        db_team = team.delete_db(team_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Team.model_validate(db_team)
