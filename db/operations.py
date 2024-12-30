"""Generic functions to create, update and delete records in the DB."""
from typing import Any, Callable, Type

from pydantic import BaseModel
from sqlalchemy.orm import Session


def create_db[T](creator: BaseModel, db_class: Type[T], session: Session) -> T:
    """
    Create a new record in the DB.

    :param creator: Creator model for the data-type.
    :type creator: BaseModel
    :param db_class: Class of the data-type.
    :type db_class: Type[T]
    :param session: Current DB session.
    :type session: Session

    :return: New DB instance.
    :rtype: T
    """
    db_item = db_class(**creator.model_dump(exclude_none=True))

    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


def update_db[T](primary_key: Any, update_model: BaseModel, reader: Callable[[Any, Session], T], session: Session) -> T:
    """
    Update an existing record in the DB.

    :param primary_key: Primary key for the record.
    :type primary_key: Any
    :param update_model: Update model for the data-type.
    :type update_model: BaseModel
    :param reader: DB retrieval function for the data-type.
    :type reader: Callable[[Any, Session], T]
    :param session: Current DB session.
    :type session: Session

    :return: Updated DB instance.
    :rtype: T

    :raise DBNotFoundError: Record does not exist.
    """
    db_item = reader(primary_key, session)

    for key, value in update_model.model_dump(exclude_none=True).items():
        setattr(db_item, key, value)

    session.commit()
    session.refresh(db_item)

    return db_item


def delete_db[T](primary_key: Any, reader: Callable[[Any, Session], T], session: Session) -> T:
    """
    Delete an existing record from the DB.

    :param primary_key: Primary key for the record.
    :type primary_key: Any
    :param reader: Retrieval function for the data-type.
    :type reader: Callable[[Any, Session], T]
    :param session: Current DB session.
    :type session: Session

    :return: Deleted DB instance.
    :rtype: T

    :raise DBNotFoundError: Record does not exist.
    """
    db_item = reader(primary_key, session)

    session.delete(db_item)
    session.commit()

    return db_item
