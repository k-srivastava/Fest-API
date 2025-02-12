"""Generate the DB schema and SQLAlchemy session."""
import base64
import os
import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Generator

import dotenv
import sqlalchemy
from sqlalchemy import Enum as SQLAlchemyEnum, Numeric, ForeignKey, orm, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session


def _generate_base64_uuid() -> str:
    """
    Generate a base64 encoded UUIDv4 for use as primary keys throughout the database.

    :return: Base64 encoded UUIDv4.
    :rtype: str
    """
    raw_uuid = uuid.uuid4()
    return base64.urlsafe_b64encode(raw_uuid.bytes).decode('utf-8').rstrip('=')


class EventType(Enum):
    """Types of events in a fest."""
    CULTURAL = 'cultural'
    E_SPORTS = 'e_sports'
    PRO_SHOW = 'pro_show'
    SPORTS = 'sports'
    TECHNICAL = 'technical'


class DBBase(DeclarativeBase):
    id: Mapped[str] = orm.mapped_column(String(22), primary_key=True, default=_generate_base64_uuid, index=True)


class DBEvent(DBBase):
    """Event table."""
    __tablename__ = 'event'

    name: Mapped[str]
    description: Mapped[Optional[str]]
    type: Mapped[EventType] = orm.mapped_column(SQLAlchemyEnum(EventType))
    team_members: Mapped[Optional[int]]
    start: Mapped[Optional[datetime]]
    venue: Mapped[Optional[str]]


class DBPass(DBBase):
    """Pass table."""
    __tablename__ = 'pass'

    name: Mapped[str]
    description: Mapped[Optional[str]]
    cost: Mapped[Decimal] = orm.mapped_column(Numeric(10, 2))


class DBTeam(DBBase):
    """Team table."""
    __tablename__ = 'team'

    name: Mapped[str] = orm.mapped_column(unique=True)
    host_id: Mapped[str] = orm.mapped_column(ForeignKey('user.id'))


class DBUser(DBBase):
    """User table."""
    __tablename__ = 'user'

    first_name: Mapped[str]
    last_name: Mapped[str]
    email_address: Mapped[str] = orm.mapped_column(unique=True)
    phone_number: Mapped[Optional[str]]
    mahe_registration_number: Mapped[Optional[int]]
    pass_id: Mapped[Optional[str]] = orm.mapped_column(ForeignKey('pass.id'))


class DBPassEvent(DBBase):
    __tablename__ = 'pass_event'

    pass_id: Mapped[str] = orm.mapped_column(ForeignKey('pass.id'))
    event_id: Mapped[str] = orm.mapped_column(ForeignKey('event.id'))


class DBTeamUser(DBBase):
    __tablename__ = 'team_user'

    team_id: Mapped[str] = orm.mapped_column(ForeignKey('team.id'))
    user_id: Mapped[str] = orm.mapped_column(ForeignKey('user.id'))


class DBTeamEvent(DBBase):
    __tablename__ = 'team_event'

    team_id: Mapped[str] = orm.mapped_column(ForeignKey('team.id'))
    event_id: Mapped[str] = orm.mapped_column(ForeignKey('event.id'))


class DBNotFoundError(Exception):
    pass


dotenv.load_dotenv()

_database_url = os.getenv('DATABASE_URL')
_engine = sqlalchemy.create_engine(_database_url)

_session_local = orm.sessionmaker(autocommit=False, autoflush=False, bind=_engine)
DBBase.metadata.create_all(bind=_engine)


def get_db() -> Generator[Session, None, None]:
    """
    Get a current DB session as a generator. The session is automatically closed after it is used.

    :return: The current DB session.
    :rtype: Generator[Session, None, None]
    """
    db = _session_local()

    try:
        yield db
    finally:
        db.close()
