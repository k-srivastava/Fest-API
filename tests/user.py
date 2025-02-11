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


class UserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        core.setup_tests(main.app)

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def assert_equal_user(
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
        self.client.post('/pass/', json=PASS_JSON)

        response = self.client.post('/user/', json=USER_JSON)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assert_equal_user(
            data, USER_JSON['first_name'], USER_JSON['last_name'], USER_JSON['email_address'],
            USER_JSON['phone_number'], USER_JSON['mahe_registration_number'], USER_JSON['pass_id']
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
            data, USER_JSON['first_name'], USER_JSON['last_name'], USER_JSON['email_address'],
            USER_JSON['phone_number'], USER_JSON['mahe_registration_number'], USER_JSON['pass_id']
        )

    def test_3_update_user(self):
        user_id = 1
        response = self.client.patch(
            f'/user/{user_id}/',
            json={'last_name': 'Doe', 'email_address': 'john.doe2025@learner.manipal.edu', 'pass_id': 1}
        )

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assert_equal_user(
            data, USER_JSON['first_name'], 'Doe', 'john.doe2025@learner.manipal.edu',
            USER_JSON['phone_number'], USER_JSON['mahe_registration_number'], 1
        )

    def test_4_read_valid_pass(self):
        user_id = 1
        pass_id = 1
        response = self.client.get(f'/user/{user_id}/pass')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assertEqual(pass_id, data['id'])
        self.assertEqual(PASS_JSON['name'], data['name'])
        self.assertEqual(PASS_JSON['description'], data['description'])
        self.assertEqual('299.00', data['cost'])

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
