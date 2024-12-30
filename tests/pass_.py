import unittest
from typing import Any

from starlette.testclient import TestClient

import main
from tests import core


class PassTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        core.setup_tests(main.app)

        cls.pass_name_json = 'Sports'
        cls.pass_description_json = 'The definitive sports pass. Access both sports and e-sports events.'
        cls.pass_cost_json = '299.00'
        cls.pass_events_json = []

        cls.new_pass_name_json = 'New Sports'
        cls.new_pass_description_json = 'The updated new sports pass. Access everything sports related.'

        cls.pass_json = {
            'name': 'Sports', 'description': 'The definitive sports pass. Access both sports and e-sports events.',
            'cost': 299, 'events': []
        }

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def assert_equal_pass(self, data: dict[str, Any], name: str, description: str, cost: str, events: list):
        self.assertEqual(name, data['name'])
        self.assertEqual(description, data['description'])
        self.assertEqual(cost, data['cost'])
        self.assertEqual(events, data['events'])

    def test_1_create_pass(self):
        response = self.client.post('/pass/', json=self.pass_json)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assert_equal_pass(
            data, self.pass_name_json, self.pass_description_json, self.pass_cost_json, self.pass_events_json
        )
        self.assertTrue('id' in data)

    def test_2_read_pass(self):
        pass_id = 1
        response = self.client.get(f'/pass/{pass_id}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assertEqual(pass_id, data['id'])
        self.assert_equal_pass(
            data, self.pass_name_json, self.pass_description_json, self.pass_cost_json, self.pass_events_json
        )

    def test_3_update_pass(self):
        pass_id = 1
        response = self.client.patch(
            f'/pass/{pass_id}/', json={'name': self.new_pass_name_json, 'description': self.new_pass_description_json}
        )

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assert_equal_pass(
            data, self.new_pass_name_json, self.new_pass_description_json, self.pass_cost_json, self.pass_events_json
        )

    def test_4_delete_pass(self):
        pass_id = 1
        response = self.client.delete(f'/pass/{pass_id}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(pass_id, data['id'])

        response = self.client.get(f'/pass/{pass_id}/')

        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(response.text)


if __name__ == '__main__':
    unittest.main()
