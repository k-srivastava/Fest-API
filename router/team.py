"""Route for all teams at /team."""
from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

import router as router_core
from db import associations, core, event, team, user
from db.core import DBNotFoundError, DBValidationError
from db.event import Event
from db.team import TeamCreate, Team, TeamUpdate
from db.user import User

router = APIRouter(prefix='/team', tags=['team'])


@router.get('/')
async def read_all_teams(db: Session = Depends(core.get_db)) -> list[Team]:
    db_teams = team.read_all_db(db)
    return [Team.model_validate(db_team) for db_team in db_teams]


@router.post('/')
async def create_team(team_create: TeamCreate, db: Session = Depends(core.get_db)) -> Team:
    db_team = team.create_db(team_create, db)
    return Team.model_validate(db_team)


@router.get('/{team_id}')
async def read_team(team_id: str, db: Session = Depends(core.get_db)) -> Team:
    try:
        db_team = team.read_db(team_id, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return Team.model_validate(db_team)


@router.get('/{team_id}/events')
async def read_team_events(team_id: str, db: Session = Depends(core.get_db)) -> list[Event]:
    try:
        event_ids = associations.read_team_events_db(team_id, db)
        db_events = event.read_by_ids_db(event_ids, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return [Event.model_validate(db_event) for db_event in db_events]


@router.post('/{team_id}/events/{event_id}')
async def create_team_event(
        team_id: str, event_id: str, validate: bool = True, validate_host_only: Optional[bool] = False,
        db: Session = Depends(core.get_db)
) -> JSONResponse:
    try:
        association_id = associations.create_team_event_db(team_id, event_id, validate, validate_host_only, db)

    except DBValidationError as e:
        raise router_core.validation_error(e)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return JSONResponse(content={'id': association_id}, status_code=status.HTTP_200_OK)


@router.delete('/{team_id}/events/{event_id}')
async def delete_team_event(team_id: str, event_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    association_id = associations.delete_team_event_db(team_id, event_id, db)
    return JSONResponse(content={'id': association_id}, status_code=status.HTTP_200_OK)


@router.get('/{team_id}/users')
async def read_team_users(team_id: str, db: Session = Depends(core.get_db)) -> list[User]:
    try:
        user_ids = associations.read_team_users_db(team_id, db)
        db_users = user.read_by_ids_db(user_ids, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return [User.model_validate(db_user) for db_user in db_users]


@router.post('/{team_id}/users/{user_id}')
async def create_team_user(team_id: str, user_id: str, validate: bool = True,
                     db: Session = Depends(core.get_db)) -> JSONResponse:
    try:
        association_id = associations.create_team_user_db(team_id, user_id, validate, db)

    except DBValidationError as e:
        raise router_core.validation_error(e)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return JSONResponse(content={'id': association_id}, status_code=status.HTTP_200_OK)


@router.delete('/{team_id}/users/{user_id}')
async def delete_team_user(team_id: str, user_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    if team.read_db(team_id, db).host_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Cannot delete host of team.')

    association_id = associations.delete_team_user_db(team_id, user_id, db)
    return JSONResponse(content={'id': association_id}, status_code=status.HTTP_200_OK)


@router.patch('/{team_id}')
async def update_team(team_id: str, team_update: TeamUpdate, db: Session = Depends(core.get_db)) -> Team:
    try:
        db_team = team.update_db(team_id, team_update, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return Team.model_validate(db_team)


@router.delete('/{team_id}')
async def delete_team(team_id: str, db: Session = Depends(core.get_db)) -> Team:
    try:
        db_team = team.delete_db(team_id, db)

    except DBNotFoundError as e:
        raise router_core.not_found_error(e)

    return Team.model_validate(db_team)
