import unittest
from typing import Any, Optional

from starlette.testclient import TestClient

import main
from tests import core


class UserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        core.setup_tests(main.app)

        cls.user_first_name_json = 'John'
        cls.user_last_name_json = 'Appleseed'
        cls.user_email_address_json = 'john.appleseed2025@learner.manipal.edu'
        cls.user_phone_number_json = 9999999999
        cls.user_mahe_registration_number = 255800000
        cls.user_pass_id_json = 1
        cls.user_teams_json = []

        cls.pass_json = {
            'name': 'Sports', 'description': 'The definitive sports pass. Access both sports and e-sports events.',
            'cost': 299, 'events': []
        }

        cls.pass_cost_string = '299.00'

        cls.user_json = {
            'first_name': 'John', 'last_name': 'Appleseed', 'email_address': 'john.appleseed2025@learner.manipal.edu',
            'phone_number': 9999999999, 'mahe_registration_number': 255800000, 'pass_id': 1, 'teams': []
        }

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def assert_equal_user(
            self, data: dict[str, Any], first_name: str, last_name: str, email_address: str,
            phone_number: Optional[int], mahe_registration_number: Optional[int], pass_id: Optional[int],
            teams: list[int]
    ):
        self.assertEqual(first_name, data['first_name'])
        self.assertEqual(last_name, data['last_name'])
        self.assertEqual(email_address, data['email_address'])
        self.assertEqual(phone_number, data['phone_number'])
        self.assertEqual(mahe_registration_number, data['mahe_registration_number'])
        self.assertEqual(pass_id, data['pass_id'])
        self.assertEqual(teams, data['teams'])

    def test_1_create_user(self):
        self.client.post('/pass/', json=self.pass_json)
        response = self.client.post('/user/', json=self.user_json)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assert_equal_user(
            data, self.user_first_name_json, self.user_last_name_json, self.user_email_address_json,
            self.user_phone_number_json, self.user_mahe_registration_number, self.user_pass_id_json,
            self.user_teams_json
        )
        self.assertTrue('id' in data)

    def test_2_read_user(self):
        user_id = 1
        response = self.client.get(f'/user/{user_id}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assertEqual(user_id, data['id'])
        self.assert_equal_user(
            data, self.user_first_name_json, self.user_last_name_json, self.user_email_address_json,
            self.user_phone_number_json, self.user_mahe_registration_number, self.user_pass_id_json,
            self.user_teams_json
        )

    def test_3_update_user(self):
        user_id = 1
        response = self.client.patch(
            f'/user/{user_id}/', json={'last_name': 'Doe', 'email_address': 'john.doe2025@learner.manipal.edu'}
        )

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assert_equal_user(
            data, self.user_first_name_json, 'Doe', 'john.doe2025@learner.manipal.edu', self.user_phone_number_json,
            self.user_mahe_registration_number, self.user_pass_id_json, self.user_teams_json
        )

    def test_4_read_valid_pass(self):
        user_id = 1
        pass_id = 1
        response = self.client.get(f'/user/{user_id}/pass')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assertEqual(pass_id, data['id'])
        self.assertEqual(self.pass_json['name'], data['name'])
        self.assertEqual(self.pass_json['description'], data['description'])
        self.assertEqual(self.pass_cost_string, data['cost'])
        self.assertEqual(self.pass_json['events'], data['events'])

    def test_5_read_invalid_pass(self):
        user_id = 1

        # Remove the pass ID from the user.
        response = self.client.patch(f'/user/{user_id}/', json={'pass_id': None})

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertIsNone(data['pass_id'])

        response = self.client.get(f'/user/{user_id}/pass')

        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(response.text)

    def test_6_delete_user(self):
        user_id = 1
        response = self.client.delete(f'/user/{user_id}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(user_id, data['id'])

        response = self.client.get(f'/user/{user_id}/')

        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(response.text)
