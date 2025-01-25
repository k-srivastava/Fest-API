"""Route for all passes at /pass."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from db import core, pass_
from db.core import DBNotFoundError
from db.pass_ import Pass, PassCreate, PassUpdate

router = APIRouter(prefix='/pass', tags=['pass'])


@router.get('/')
def read_all_passes(db: Session = Depends(core.get_db)) -> list[Pass]:
    db_passes = pass_.read_all_db(db)
    return [Pass.model_validate(db_pass) for db_pass in db_passes]


@router.post('/')
def create_pass(pass_create: PassCreate, db: Session = Depends(core.get_db)) -> Pass:
    db_pass = pass_.create_db(pass_create, db)
    return Pass.model_validate(db_pass)


@router.get('/{pass_id}')
def read_pass(pass_id: int, db: Session = Depends(core.get_db)) -> Pass:
    try:
        db_pass = pass_.read_db(pass_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Pass.model_validate(db_pass)


@router.patch('/{pass_id}')
def update_pass(pass_id: int, pass_update: PassUpdate, db: Session = Depends(core.get_db)) -> Pass:
    try:
        db_pass = pass_.update_db(pass_id, pass_update, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Pass.model_validate(db_pass)


@router.delete('/{pass_id}')
def delete_pass(pass_id: int, db: Session = Depends(core.get_db)) -> Pass:
    try:
        db_pass = pass_.delete_db(pass_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Pass.model_validate(db_pass)
