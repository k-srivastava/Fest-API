import unittest
from typing import Any, Optional

from starlette.testclient import TestClient

import main
from tests import core

USER_JSON = {
    'first_name': 'John', 'last_name': 'Appleseed', 'email_address': 'john.appleseed2025@learner.manipal.edu',
    'phone_number': '9999999999', 'mahe_registration_number': 255800000, 'pass_id': None
}

NEW_USER_JSON = {
    'first_name': 'Jane', 'last_name': 'Smith', 'email_address': 'jane.smith2024@learner.manipal.edu',
    'phone_number': None, 'mahe_registration_number': 255899999, 'pass_id': None
}

TEAM_JSON = {'name': 'Team 1', 'host_id': 1}

TEAM_ID: Optional[int] = None


class TeamTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        core.setup_tests(main.app)

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def assert_team_is_equal(self, data: dict[str, Any], name: str, host_id: int):
        self.assertEqual(name, data['name'])
        self.assertEqual(host_id, data['host_id'])

    def test_1_create_team(self):
        self.client.post('/user/', json=USER_JSON)

        response = self.client.post('/team/', json=TEAM_JSON)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assert_team_is_equal(data, 'Team 1', 1)
        self.assertTrue('id' in data)

        global TEAM_ID
        TEAM_ID = data['id']

    def test_2_read_team(self):
        response = self.client.get(f'/team/{TEAM_ID}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assertEqual(TEAM_ID, data['id'])
        self.assert_team_is_equal(data, 'Team 1', 1)

    def test_3_update_team(self):
        self.client.post('/user/', json=NEW_USER_JSON)
        response = self.client.patch(f'/team/{TEAM_ID}/', json={'name': 'New Team 1', 'host_id': 2})

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assert_team_is_equal(data, 'New Team 1', 2)

    def test_4_delete_team(self):
        response = self.client.delete(f'/team/{TEAM_ID}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(TEAM_ID, data['id'])

        response = self.client.get(f'/team/{TEAM_ID}/')
        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(response.text)
