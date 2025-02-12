"""Generate the DB schema and SQLAlchemy session for testing."""
from typing import Generator

import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import StaticPool, orm
from sqlalchemy.orm import Session

from db import core
from db.core import DBBase, DBPass, DBEvent, DBPassEvent, DBTeam, DBTeamEvent, DBTeamUser, DBUser

_DATABASE_URL = 'sqlite:///:memory:'
_test_engine = sqlalchemy.create_engine(_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool)
_test_session_local = orm.sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


def get_test_db() -> Generator[Session, None, None]:
    """
    Get a current test DB session as a generator. The session is automatically closed after it is used.

    :return: The current test DB session.
    :rtype: Generator[Session, None, None]
    """
    db = _test_session_local()

    try:
        yield db
    finally:
        db.close()


# noinspection SpellCheckingInspection
def create_default_test_db():
    """Create some default test data; useful for testing associations between entities."""
    events = [
        {
            "name": "DJ Night",
            "description": "Party in the evening with song and dance.",
            "type": "PRO_SHOW",
            "team_members": None,
            "start": None,
            "venue": None,
            "id": "TSK4dI3xTaCMBNqVCF_whg"
        },

        {
            "name": "CodeJam",
            "description": "Short-paced coding challenges to tickle the brain.",
            "type": "TECHNICAL",
            "team_members": 3,
            "start": None,
            "venue": None,
            "id": "qkjB9pe1QNqn-HeZyJHhtg"
        },

        {
            "name": "Track&Field",
            "description": "Battle it out on the track.",
            "type": "SPORTS",
            "team_members": 5,
            "start": None,
            "venue": None,
            "id": "BR2PlUXzRKO8FKwsq3oh5Q"
        },

        {
            "name": "E-Sports Mania",
            "description": "Play out in various tournaments.",
            "type": "E_SPORTS",
            "team_members": 2,
            "start": None,
            "venue": None,
            "id": "lu943W-NRQC5TvVLQOBA1w"
        }
    ]

    passes = [
        {
            "name": "Sports Pass", "description": "Access all the sporting events.", "cost": 299.00,
            "id": "glcuybQXQPOPG1pxVhLpGQ"
        },

        {
            "name": "All Sports Pass", "description": "Access both sports and e-sports events.", "cost": 399.00,
            "id": "v1rYrkgMQ92a96ri8Xmegg"
        },

        {
            "name": "Cultured Pass", "description": "Access all cultural events.", "cost": 599.00,
            "id": "VgJn2YB6S-yIzw4qd174ig"
        },

        {
            "name": "Technical Pass", "description": "Access all technical events.", "cost": 399.00,
            "id": "Ohgl0KJ8SuCX4MujKocDhQ"
        },

        {
            "name": "All Access Pass", "description": "Access every single event in the fest.", "cost": 799.00,
            "id": "6kiwVr6USIyuIqWWWJJ_yg"
        },

        {
            "name": "Proshow Pass", "description": "Access the party at the proshow.", "cost": 499.00,
            "id": "xD8s_FCsSE2BmFzurYyTvA"
        }
    ]

    pass_events = [
        {
            "event_id": "TSK4dI3xTaCMBNqVCF_whg",
            "pass_id": "xD8s_FCsSE2BmFzurYyTvA",
            "id": "AAELCQb6ThizbRj_GjQ4eg"
        },

        {
            "event_id": "TSK4dI3xTaCMBNqVCF_whg",
            "pass_id": "6kiwVr6USIyuIqWWWJJ_yg",
            "id": "bZosWKWKRH2CZr3-BUMxIA"
        },

        {
            "event_id": "qkjB9pe1QNqn-HeZyJHhtg",
            "pass_id": "Ohgl0KJ8SuCX4MujKocDhQ",
            "id": "9OxETRSDQciiYguWLVIMdg"
        },

        {
            "event_id": "qkjB9pe1QNqn-HeZyJHhtg",
            "pass_id": "6kiwVr6USIyuIqWWWJJ_yg",
            "id": "ZMc94xMOQjm6bxZ4LYAfdQ"
        },

        {
            "event_id": "BR2PlUXzRKO8FKwsq3oh5Q",
            "pass_id": "glcuybQXQPOPG1pxVhLpGQ",
            "id": "G8tA-6QFQPKOsGZ_e5folA"
        },

        {
            "event_id": "BR2PlUXzRKO8FKwsq3oh5Q",
            "pass_id": "v1rYrkgMQ92a96ri8Xmegg",
            "id": "SQors1RxTkSpgE0Jcq4D_w"
        },

        {
            "event_id": "BR2PlUXzRKO8FKwsq3oh5Q",
            "pass_id": "6kiwVr6USIyuIqWWWJJ_yg",
            "id": "fbq0owIPTBCYaB17Z26CJg"
        },

        {
            "event_id": "lu943W-NRQC5TvVLQOBA1w",
            "pass_id": "v1rYrkgMQ92a96ri8Xmegg",
            "id": "7R2j3XvQTqiikQb-dVx5fg"
        },

        {
            "event_id": "lu943W-NRQC5TvVLQOBA1w",
            "pass_id": "6kiwVr6USIyuIqWWWJJ_yg",
            "id": "ENdJ5ipZSgSlPzf2NzWTKg"
        }
    ]

    teams = [
        {
            "name": "Sports Champs",
            "host_id": "5hYNA08sSUmQKV91kqTFvQ",
            "id": "yNWqAe1qSOGKzUq6o1XkTw"
        },

        {
            "name": "Stardust Crusaders",
            "host_id": "5hYNA08sSUmQKV91kqTFvQ",
            "id": "ETjnsxhqRsGNFqEV_ZuCuA"
        },

        {
            "name": "Diamonds are Forever",
            "host_id": "tZcRIaIpTeuap8n7L8vqOw",
            "id": "5yZJrI-yTmqcKM6pR1BIbQ"
        }
    ]

    team_events = [
        {
            "team_id": "yNWqAe1qSOGKzUq6o1XkTw",
            "event_id": "BR2PlUXzRKO8FKwsq3oh5Q",
            "id": "DoGWnYYZQSiNs5AbwleUpA"
        },

        {
            "team_id": "5yZJrI-yTmqcKM6pR1BIbQ",
            "event_id": "qkjB9pe1QNqn-HeZyJHhtg",
            "id": "oEHc8OXiRb-K-O7ivIpIGA"
        }
    ]

    team_users = [
        {
            "team_id": "yNWqAe1qSOGKzUq6o1XkTw",
            "user_id": "5hYNA08sSUmQKV91kqTFvQ",
            "id": "vj-y_PoQQSWKZ-ERUlLTyQ"
        },

        {
            "team_id": "yNWqAe1qSOGKzUq6o1XkTw",
            "user_id": "tZcRIaIpTeuap8n7L8vqOw",
            "id": "4wjboEe9S2eo2r-PkSfpPQ"
        },

        {
            "team_id": "ETjnsxhqRsGNFqEV_ZuCuA",
            "user_id": "5hYNA08sSUmQKV91kqTFvQ",
            "id": "XXKRaFkaTzqSb7GJPhkJ-Q"
        },

        {
            "team_id": "5yZJrI-yTmqcKM6pR1BIbQ",
            "user_id": "tZcRIaIpTeuap8n7L8vqOw",
            "id": "vthd-i_TSxGZ8IokKMOiUw"
        }
    ]

    users = [
        {
            "first_name": "John",
            "last_name": "Smith",
            "email_address": "john.smith2025@learner.manipal.edu",
            "phone_number": "9876543210",
            "mahe_registration_number": 225805000,
            "pass_id": "v1rYrkgMQ92a96ri8Xmegg",
            "id": "5hYNA08sSUmQKV91kqTFvQ"
        },

        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email_address": "jane.doe2022@learner.manipal.edu",
            "phone_number": "1234567890",
            "mahe_registration_number": 225805999,
            "pass_id": "6kiwVr6USIyuIqWWWJJ_yg",
            "id": "tZcRIaIpTeuap8n7L8vqOw"
        }
    ]

    db = _test_session_local()

    db.execute(sqlalchemy.insert(DBEvent).values(events))
    db.execute(sqlalchemy.insert(DBPass).values(passes))
    db.execute(sqlalchemy.insert(DBPassEvent).values(pass_events))
    db.execute(sqlalchemy.insert(DBTeam).values(teams))
    db.execute(sqlalchemy.insert(DBTeamEvent).values(team_events))
    db.execute(sqlalchemy.insert(DBTeamUser).values(team_users))
    db.execute(sqlalchemy.insert(DBUser).values(users))

    db.commit()
    db.close()


def get_default_db_ids() -> dict[str, str]:
    """
    Get the IDs of some default DB entities. Useful in conjunction with the `create_default_test_db` function.

    :return: Dictionary of relevant DB entity IDs.
    :rtype: dict[str, str]
    """
    # noinspection SpellCheckingInspection
    return {
        'track&field-event': 'BR2PlUXzRKO8FKwsq3oh5Q',
        'all-sports-pass': 'v1rYrkgMQ92a96ri8Xmegg',
        'sports-champs-team': 'yNWqAe1qSOGKzUq6o1XkTw',
        'john-smith-user': '5hYNA08sSUmQKV91kqTFvQ'
    }


def setup_tests(app: FastAPI):
    """
    Override the app production DB dependency with the test DB and create the schema.

    :param app: App in which the test DB dependency will be overridden.
    :type app: FastAPI
    """
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[core.get_db] = get_test_db
    DBBase.metadata.create_all(bind=_test_engine)


def teardown_tests():
    """Drop all tables from the schema."""
    DBBase.metadata.drop_all(bind=_test_engine)
