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
    EXPERIENCES = 'experiences'
    FINANCE = 'finance'
    HACKATHON = 'hackathon'
    OTHER = 'other'
    PRO_SHOW = 'pro_show'
    ROBOTICS = 'robotics'
    SPORTS = 'sports'
    TECHNICAL = 'technical'


class SupportTicketCategory(Enum):
    """Types of support ticket categories."""
    CONTEST = 'contest'
    EVENT = 'event'
    ORGANIZATION = 'organization'
    OTHER = 'other'
    PASSES = 'passes'
    PAYMENT = 'payment'
    SPECIAL_REQUEST = 'special_request'
    WEBSITE = 'website'


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
    organizer_id: Mapped[Optional[str]] = orm.mapped_column(ForeignKey('user.id', ondelete='CASCADE'))


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
    host_id: Mapped[str] = orm.mapped_column(ForeignKey('user.id', ondelete='CASCADE'))


class DBUser(DBBase):
    """User table."""
    __tablename__ = 'user'

    first_name: Mapped[str]
    last_name: Mapped[str]
    email_address: Mapped[str] = orm.mapped_column(unique=True)
    phone_number: Mapped[Optional[str]]
    mahe_registration_number: Mapped[Optional[int]]
    pass_id: Mapped[Optional[str]] = orm.mapped_column(ForeignKey('pass.id', ondelete='CASCADE'))


class DBSupportTicket(DBBase):
    """Support ticket table."""
    __tablename__ = 'support_ticket'

    name: Mapped[str]
    description: Mapped[str]
    category: Mapped[SupportTicketCategory] = orm.mapped_column(SQLAlchemyEnum(SupportTicketCategory))
    timestamp: Mapped[datetime]
    solved: Mapped[bool]
    college_name: Mapped[Optional[str]]
    email_address: Mapped[Optional[str]]
    phone_number: Mapped[Optional[str]]
    solved_email_address: Mapped[Optional[str]]


class DBPassEvent(DBBase):
    """Pass and event association table."""
    __tablename__ = 'pass_event'

    pass_id: Mapped[str] = orm.mapped_column(ForeignKey('pass.id', ondelete='CASCADE'))
    event_id: Mapped[str] = orm.mapped_column(ForeignKey('event.id', ondelete='CASCADE'))


class DBTeamUser(DBBase):
    """Team and user association table."""
    __tablename__ = 'team_user'

    team_id: Mapped[str] = orm.mapped_column(ForeignKey('team.id', ondelete='CASCADE'))
    user_id: Mapped[str] = orm.mapped_column(ForeignKey('user.id', ondelete='CASCADE'))


class DBTeamEvent(DBBase):
    """Team and event association table."""
    __tablename__ = 'team_event'

    team_id: Mapped[str] = orm.mapped_column(ForeignKey('team.id', ondelete='CASCADE'))
    event_id: Mapped[str] = orm.mapped_column(ForeignKey('event.id', ondelete='CASCADE'))


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
