"""Route for all teams at /team."""
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from db import core, team
from db.core import DBNotFoundError
from db.team import TeamCreate, Team, TeamUpdate

router = APIRouter(prefix='/team', tags=['team'])


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
