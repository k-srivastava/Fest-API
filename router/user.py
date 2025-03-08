"""Route for all users at /user."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, StreamingResponse, Response

from db import core, event, user, pass_, team, associations
from db.core import DBNotFoundError, DBValidationError
from db.event import Event
from db.pass_ import Pass
from db.team import Team
from db.user import UserCreate, User, UserUpdate

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/')
def create_user(user_create: UserCreate, db: Session = Depends(core.get_db)) -> User:
    db_user = user.create_db(user_create, db)
    return User.model_validate(db_user)


@router.get('/id')
def read_user_id_from_email_address(email_address: str, db: Session = Depends(core.get_db)) -> str:
    try:
        user_id = user.read_id_from_email_address_db(email_address, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return user_id


@router.get('/id-registration')
def read_user_id_from_mahe_registration_number(
        mahe_registration_number: int, db: Session = Depends(core.get_db)
) -> str:
    try:
        user_id = user.read_id_from_mahe_registration_number_db(mahe_registration_number, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return user_id


@router.get('/{user_id}')
def read_user(user_id: str, db: Session = Depends(core.get_db)) -> User:
    try:
        db_user = user.read_db(user_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return User.model_validate(db_user)


@router.get('/{user_id}/qr_code')
def read_user_qr_code(user_id: str, db: Session = Depends(core.get_db)) -> Response:
    try:
        bytes_stream = user.create_qr_code(user_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return StreamingResponse(bytes_stream, media_type='image/png')


@router.get('/{user_id}/pass')
def read_user_pass(user_id: str, db: Session = Depends(core.get_db)) -> Pass:
    try:
        pass_id = user.read_pass_db(user_id, db)
        db_pass = pass_.read_db(pass_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Pass.model_validate(db_pass)


@router.get('/{user_id}/events')
def read_user_events(user_id: str, db: Session = Depends(core.get_db)) -> list[Event]:
    try:
        event_ids = user.read_events_organizer_db(user_id, db)
        db_events = [event.read_db(event_id, db) for event_id in event_ids]

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return [Event.model_validate(db_event) for db_event in db_events]


@router.get('/{user_id}/teams')
def read_user_teams(user_id: str, host: bool, db: Session = Depends(core.get_db)) -> list[Team]:
    try:
        if host:
            team_ids = user.read_teams_host_db(user_id, db)
        else:
            team_ids = associations.read_user_teams_db(user_id, db)

        db_teams = [team.read_db(team_id, db) for team_id in team_ids]

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return [Team.model_validate(db_team) for db_team in db_teams]


@router.post('/{user_id}/teams/{team_id}')
def create_user_team(user_id: str, team_id: str, validate: bool = True,
                     db: Session = Depends(core.get_db)) -> JSONResponse:
    try:
        association_id = associations.create_team_user_db(team_id, user_id, validate, db)

    except DBValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return JSONResponse(content={'id': association_id}, status_code=200)


@router.delete('/{user_id}/teams/{team_id}')
def delete_user_team(user_id: str, team_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    if team.read_db(team_id, db).host_id == user_id:
        raise HTTPException(status_code=403, detail='Cannot delete host of team.')

    association_id = associations.delete_team_user_db(team_id, user_id, db)
    return JSONResponse(content={'id': association_id}, status_code=200)


@router.get('/{user_id}/events')
def read_user_events(user_id: str, db: Session = Depends(core.get_db)) -> list[Event]:
    try:
        event_ids = associations.read_user_events_db(user_id, db)
        db_events = [event.read_db(event_id, db) for event_id in event_ids]

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return [Event.model_validate(db_event) for db_event in db_events]


@router.post('/{user_id}/events/{event_id}')
def create_user_event(
        user_id: str, event_id: str, validate: bool = True, db: Session = Depends(core.get_db)
) -> JSONResponse:
    try:
        association_id = associations.create_user_event_db(user_id, event_id, validate, db)

    except DBValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return JSONResponse(content={'id': association_id}, status_code=200)


@router.delete('/{user_id}/events/{event_id}')
def delete_user_event(user_id: str, event_id: str, db: Session = Depends(core.get_db)) -> JSONResponse:
    association_id = associations.delete_user_event_db(user_id, event_id, db)
    return JSONResponse(content={'id': association_id}, status_code=200)


@router.patch('/{user_id}')
def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(core.get_db)) -> User:
    try:
        db_user = user.update_db(user_id, user_update, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return User.model_validate(db_user)


@router.delete('/{user_id}')
def delete_user(user_id: str, db: Session = Depends(core.get_db)) -> User:
    try:
        db_user = user.delete_db(user_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return User.model_validate(db_user)
