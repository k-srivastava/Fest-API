import datetime
import unittest
from typing import Optional

from starlette.testclient import TestClient

import main
from db.core import EventType
from tests import core

EVENT_JSON = {
    'name': 'Battle of Bands', 'description': 'A competition between the best bands on campus.',
    'type': EventType.CULTURAL.value, 'team_members': 5, 'start': datetime.datetime(2025, 1, 1, 12, 0, 0).isoformat(),
    'venue': 'Mega Auditorium'
}


class EventTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        core.setup_tests(main.app)

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def assert_event_is_equal(
            self, data: dict[str, any], name: str, description: Optional[str], type_: EventType,
            team_members: Optional[int], start: Optional[str], venue: Optional[str]
    ):
        self.assertEqual(name, data['name'])
        self.assertEqual(description, data['description'])
        self.assertEqual(type_, data['type'])
        self.assertEqual(team_members, data['team_members'])
        self.assertEqual(start, data['start'])
        self.assertEqual(venue, data['venue'])

    def test_1_create_event(self):
        response = self.client.post('/event/', json=EVENT_JSON)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assert_event_is_equal(
            data, EVENT_JSON['name'], EVENT_JSON['description'], EVENT_JSON['type'], EVENT_JSON['team_members'],
            EVENT_JSON['start'], EVENT_JSON['venue']
        )
        self.assertTrue('id' in data)

    def test_2_read_event(self):
        event_id = 1
        response = self.client.get(f'/event/{event_id}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assertEqual(event_id, data['id'])
        self.assert_event_is_equal(
            data, EVENT_JSON['name'], EVENT_JSON['description'], EVENT_JSON['type'], EVENT_JSON['team_members'],
            EVENT_JSON['start'], EVENT_JSON['venue']
        )

    def test_3_update_event(self):
        event_id = 1
        response = self.client.patch(f'/event/{event_id}/', json={'type': EventType.PRO_SHOW.value, 'venue': None})

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assert_event_is_equal(
            data, EVENT_JSON['name'], EVENT_JSON['description'], EventType.PRO_SHOW.value, EVENT_JSON['team_members'],
            EVENT_JSON['start'], None
        )

    def test_4_delete_event(self):
        event_id = 1
        response = self.client.delete(f'/event/{event_id}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(event_id, data['id'])

        response = self.client.get(f'/event/{event_id}/')

        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(response.text)
