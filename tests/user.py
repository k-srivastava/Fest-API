import unittest
from decimal import Decimal
from typing import Any, Optional

from starlette.testclient import TestClient

import main
from tests import core

PASS_JSON = {
    'name': 'Sports', 'description': 'The definitive sports pass. Access both sports and e-sports events.',
    'cost': Decimal(299).to_eng_string()
}

USER_JSON = {
    'first_name': 'John', 'last_name': 'Appleseed', 'email_address': 'john.appleseed2025@learner.manipal.edu',
    'phone_number': '9999999999', 'mahe_registration_number': 255800000, 'pass_id': None
}

TEAM_1_JSON = {'name': 'Team 1', 'host_id': None}
TEAM_2_JSON = {'name': 'Team 2', 'host_id': None}

PASS_ID: Optional[str] = None
USER_ID: Optional[str] = None


class UserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        cls.headers = core.get_default_headers()

        core.setup_tests(main.app)

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def assert_user_is_equal(
            self, data: dict[str, Any], first_name: str, last_name: str, email_address: str,
            phone_number: Optional[str], mahe_registration_number: Optional[int], pass_id: Optional[int]
    ):
        self.assertEqual(first_name, data['first_name'])
        self.assertEqual(last_name, data['last_name'])
        self.assertEqual(email_address, data['email_address'])
        self.assertEqual(phone_number, data['phone_number'])
        self.assertEqual(mahe_registration_number, data['mahe_registration_number'])
        self.assertEqual(pass_id, data['pass_id'])

    def test_1_create_user(self):
        response = self.client.post('/pass/', json=PASS_JSON, headers=self.headers)
        data = response.json()

        global PASS_ID
        PASS_ID = data['id']

        response = self.client.post('/user/', json=USER_JSON, headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assert_user_is_equal(
            data, USER_JSON['first_name'], USER_JSON['last_name'], USER_JSON['email_address'],
            USER_JSON['phone_number'], USER_JSON['mahe_registration_number'], USER_JSON['pass_id']
        )
        self.assertTrue('id' in data)

        global USER_ID
        USER_ID = data['id']

    def test_2_read_user(self):
        response = self.client.get(f'/user/{USER_ID}/', headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assertEqual(USER_ID, data['id'])
        self.assert_user_is_equal(
            data, USER_JSON['first_name'], USER_JSON['last_name'], USER_JSON['email_address'],
            USER_JSON['phone_number'], USER_JSON['mahe_registration_number'], USER_JSON['pass_id']
        )

    def test_3_read_user_id(self):
        response = self.client.get(
            '/user/id', params={'email_address': USER_JSON['email_address']}, headers=self.headers
        )

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(USER_ID, data)

    def test_4_update_user(self):
        response = self.client.patch(
            f'/user/{USER_ID}/',
            json={'last_name': 'Doe', 'email_address': 'john.doe2025@learner.manipal.edu', 'pass_id': PASS_ID},
            headers=self.headers
        )

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assert_user_is_equal(
            data, USER_JSON['first_name'], 'Doe', 'john.doe2025@learner.manipal.edu',
            USER_JSON['phone_number'], USER_JSON['mahe_registration_number'], PASS_ID
        )

    def test_5_read_valid_pass(self):
        response = self.client.get(f'/user/{USER_ID}/pass', headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assertEqual(PASS_ID, data['id'])
        self.assertEqual(PASS_JSON['name'], data['name'])
        self.assertEqual(PASS_JSON['description'], data['description'])
        self.assertEqual('299.00', data['cost'])

    def test_6_read_invalid_pass(self):
        # Remove the pass ID from the user.
        response = self.client.patch(f'/user/{USER_ID}/', json={'pass_id': None}, headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertIsNone(data['pass_id'])

        response = self.client.get(f'/user/{USER_ID}/pass', headers=self.headers)

        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(response.text)

    def test_7_read_empty_team_host(self):
        response = self.client.get(f'/user/{USER_ID}/teams', headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(0, len(data))

    def test_8_read_valid_team_host(self):
        TEAM_1_JSON['host_id'] = USER_ID
        TEAM_2_JSON['host_id'] = USER_ID

        self.client.post('/team/', json=TEAM_1_JSON, headers=self.headers)
        self.client.post('/team/', json=TEAM_2_JSON, headers=self.headers)

        response = self.client.get(f'/user/{USER_ID}/teams', headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(2, len(data))

        self.assertEqual(TEAM_1_JSON['name'], data[0]['name'])
        self.assertEqual(TEAM_1_JSON['host_id'], data[0]['host_id'])

        self.assertEqual(TEAM_2_JSON['name'], data[1]['name'])
        self.assertEqual(TEAM_2_JSON['host_id'], data[1]['host_id'])

    def test_9_delete_user(self):
        response = self.client.delete(f'/user/{USER_ID}/', headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(USER_ID, data['id'])

        response = self.client.get(f'/user/{USER_ID}/', headers=self.headers)

        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(response.text)
