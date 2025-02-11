"""Route for all users at /user."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from db import core, user, pass_
from db.core import DBNotFoundError
from db.pass_ import Pass
from db.user import UserCreate, User, UserUpdate

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/')
def create_user(user_create: UserCreate, db: Session = Depends(core.get_db)) -> User:
    db_user = user.create_db(user_create, db)
    return User.model_validate(db_user)


@router.get('/{user_id}')
def read_user(user_id: str, db: Session = Depends(core.get_db)) -> User:
    try:
        db_user = user.read_db(user_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return User.model_validate(db_user)


@router.get('/{user_id}/pass')
def read_user_pass(user_id: str, db: Session = Depends(core.get_db)) -> Pass:
    try:
        pass_id = user.read_pass_db(user_id, db)
        db_pass = pass_.read_db(pass_id, db)

    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Pass.model_validate(db_pass)


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
