"""Generate the DB schema and SQLAlchemy session."""
import os
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Generator

import dotenv
import sqlalchemy
from sqlalchemy import Enum as SQLAlchemyEnum, Numeric, Table, Column, ForeignKey, orm
from sqlalchemy.orm import DeclarativeBase, Mapped, Session


class EventType(Enum):
    """Types of events in a fest."""
    CULTURAL = 'cultural'
    E_SPORTS = 'e_sports'
    PRO_SHOW = 'pro_show'
    SPORTS = 'sports'
    TECHNICAL = 'technical'


class DBBase(DeclarativeBase):
    pass


# Many-to-many relationship between a pass and event.
_pass_event_association = Table(
    'event_pass_association',
    DBBase.metadata,
    Column('pass_id', ForeignKey('pass.id'), primary_key=True),
    Column('event_id', ForeignKey('event.id'), primary_key=True)
)

# Many-to-many relationship between a user and team.
_user_team_association = Table(
    'user_team_association',
    DBBase.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('team_id', ForeignKey('team.id'), primary_key=True)
)


class DBEvent(DBBase):
    """Event table."""
    __tablename__ = 'event'

    id: Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    type: Mapped[EventType] = orm.mapped_column(SQLAlchemyEnum(EventType))
    team_members: Mapped[Optional[int]]
    start: Mapped[Optional[datetime]]
    venue: Mapped[Optional[str]]

    # List of passes that can access this event.
    passes: Mapped[list['DBPass']] = orm.relationship(
        'DBPass', secondary=_pass_event_association, back_populates='events'
    )


class DBPass(DBBase):
    """Pass table."""
    __tablename__ = 'pass'

    id: Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    cost: Mapped[Decimal] = orm.mapped_column(Numeric(10, 2))

    # List of events that can be accessed by this pass.
    events: Mapped[list['DBEvent']] = orm.relationship(
        'DBEvent', secondary=_pass_event_association, back_populates='passes'
    )


class DBTeam(DBBase):
    """Team table."""
    __tablename__ = 'team'

    id: Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    name: Mapped[str] = orm.mapped_column(unique=True)
    host_id: Mapped[int] = orm.mapped_column(ForeignKey('user.id'))

    # List of members of this team.
    members: Mapped[list['DBUser']] = orm.relationship(
        'DBUser', secondary=_user_team_association, back_populates='teams'
    )


class DBUser(DBBase):
    """User table."""
    __tablename__ = 'user'

    id: Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email_address: Mapped[str] = orm.mapped_column(unique=True)
    phone_number: Mapped[Optional[int]]
    mahe_registration_number: Mapped[Optional[int]]
    pass_id: Mapped[Optional[int]] = orm.mapped_column(ForeignKey('pass.id'))

    # List of teams this user is a member of.
    teams: Mapped[list['DBTeam']] = orm.relationship(
        'DBTeam', secondary=_user_team_association, back_populates='members'
    )


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
